"""Core feature and history primitives for the modeling engine."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4

from GEOMETRY.point import Point3D
from MODELING.body import ModelBody


class FeatureType(str, Enum):
    """Supported parametric feature operations."""

    EXTRUDE = "extrude"
    REVOLVE = "revolve"
    SWEEP = "sweep"
    LOFT = "loft"
    SHELL = "shell"
    DRAFT = "draft"
    RIB = "rib"
    HOLE = "hole"
    THREAD = "thread"
    PATTERN = "pattern"
    MIRROR = "mirror"
    BOOLEAN_UNION = "boolean_union"
    BOOLEAN_SUBTRACT = "boolean_subtract"
    BOOLEAN_INTERSECT = "boolean_intersect"
    SPLIT_BODY = "split_body"
    COMBINE_BODIES = "combine_bodies"
    OFFSET_FACE = "offset_face"
    REPLACE_FACE = "replace_face"
    DELETE_FACE = "delete_face"


@dataclass(slots=True)
class ReferenceGeometry:
    """Reference geometry descriptor."""

    name: str
    geometry_type: str


@dataclass(slots=True)
class WorkPlane:
    """Work plane descriptor."""

    name: str
    origin: Point3D
    normal: tuple[float, float, float]


@dataclass(slots=True)
class WorkAxis:
    """Work axis descriptor."""

    name: str
    direction: tuple[float, float, float]


@dataclass(slots=True)
class WorkPoint:
    """Work point descriptor."""

    name: str
    point: Point3D


@dataclass(slots=True)
class Feature:
    """A parametric feature definition."""

    feature_id: str
    name: str
    feature_type: FeatureType
    parameters: dict[str, Any] = field(default_factory=dict)
    suppressed: bool = False
    dependencies: tuple[str, ...] = field(default_factory=tuple)


class FeatureTree:
    """Ordered feature tree for a part model."""

    def __init__(self) -> None:
        self._features: list[Feature] = []

    def set_features(self, features: list[Feature]) -> None:
        """Replace the feature collection."""
        self._features = list(features)

    def add(self, feature: Feature) -> None:
        """Append a feature to the tree."""
        self._features.append(feature)

    def feature_names(self) -> list[str]:
        """Return feature names in tree order."""
        return [feature.name for feature in self._features]

    def feature_count(self) -> int:
        """Return the number of features."""
        return len(self._features)

    def find_by_name(self, name: str) -> Feature:
        """Return a feature by name."""
        for feature in self._features:
            if feature.name == name:
                return feature
        raise KeyError(f"Feature '{name}' was not found")


class ParametricHistory:
    """Capture regeneration snapshots for rollback and inspection."""

    def __init__(self) -> None:
        self._snapshots: list[dict[str, Any]] = []

    def clear(self) -> None:
        """Clear stored history snapshots."""
        self._snapshots.clear()

    def record(self, snapshot: dict[str, Any]) -> None:
        """Record a regeneration snapshot."""
        self._snapshots.append(deepcopy(snapshot))

    def snapshots(self) -> list[dict[str, Any]]:
        """Return recorded snapshots."""
        return list(self._snapshots)


class DesignHistory:
    """Capture user-facing feature application history."""

    def __init__(self) -> None:
        self._entries: list[dict[str, Any]] = []

    def clear(self) -> None:
        """Clear design-history entries."""
        self._entries.clear()

    def record(self, feature: Feature, body: ModelBody) -> None:
        """Record a feature application result."""
        self._entries.append({"feature": feature.name, "type": feature.feature_type.value, "volume": body.volume})

    def entries(self) -> list[dict[str, Any]]:
        """Return the design-history entries."""
        return list(self._entries)


@dataclass(slots=True)
class RegenerationResult:
    """Result of a parametric model regeneration pass."""

    converged: bool
    iterations: int
    residual: float = 0.0


class FeatureManager:
    """Manage features, regeneration, rollback, and undo/redo."""

    def __init__(self) -> None:
        self._features: list[Feature] = []
        self.feature_tree = FeatureTree()
        self._undo_stack: list[dict[str, Any]] = []
        self._redo_stack: list[dict[str, Any]] = []
        self._rollback_name: str | None = None

    def create_feature(self, feature_type: FeatureType, name: str, parameters: dict[str, Any], dependencies: tuple[str, ...] = ()) -> Feature:
        """Create and register a feature definition."""
        self._push_undo_state()
        feature = Feature(feature_id=str(uuid4()), name=name, feature_type=feature_type, parameters=dict(parameters), dependencies=tuple(dependencies))
        self._features.append(feature)
        self.feature_tree.set_features(self._features)
        return feature

    def edit_feature(self, feature_id: str, **updates: Any) -> Feature:
        """Edit a feature's parameters."""
        self._push_undo_state()
        feature = self._get_feature(feature_id)
        feature.parameters.update(updates)
        return feature

    def suppress_feature(self, feature_id: str, suppressed: bool) -> None:
        """Suppress or unsuppress a feature."""
        self._push_undo_state()
        self._get_feature(feature_id).suppressed = suppressed

    def rollback_to(self, feature_name: str) -> bool:
        """Rollback regeneration visibility to the named feature."""
        self._rollback_name = feature_name
        return True

    def regenerate(self, part: "PartModel") -> RegenerationResult:
        """Regenerate the part by replaying visible, unsuppressed features."""
        from MODELING.extrude import apply_extrude
        from MODELING.loft import apply_loft
        from MODELING.pattern import apply_pattern
        from MODELING.revolve import apply_revolve
        from MODELING.shell import apply_shell
        from MODELING.sweep import apply_sweep
        from MODELING.boolean import BooleanOperation

        active_features = self._active_features()
        body = ModelBody(name=f"{part.name}-body", volume=0.0, face_count=0, edge_count=0, body_count=0)
        iterations = 0
        part.parametric_history.clear()
        part.design_history.clear()
        for feature in active_features:
            if feature.suppressed:
                continue
            iterations += 1
            feature_type = feature.feature_type
            if feature_type == FeatureType.EXTRUDE:
                body = apply_extrude(part, body, feature.parameters)
            elif feature_type == FeatureType.REVOLVE:
                body = apply_revolve(part, body, feature.parameters)
            elif feature_type == FeatureType.SWEEP:
                body = apply_sweep(part, body, feature.parameters)
            elif feature_type == FeatureType.LOFT:
                body = apply_loft(part, body, feature.parameters)
            elif feature_type == FeatureType.SHELL:
                body = apply_shell(body, feature.parameters)
            elif feature_type == FeatureType.DRAFT:
                body.volume *= max(0.1, 1.0 - float(feature.parameters.get("angle", 0.0)) * 0.005)
            elif feature_type == FeatureType.RIB:
                body.volume += float(feature.parameters.get("thickness", 0.0)) * float(feature.parameters.get("length", 0.0)) * 2.0
                body.face_count += 2
                body.edge_count += 4
            elif feature_type == FeatureType.HOLE:
                diameter = float(feature.parameters.get("diameter", 0.0))
                depth = float(feature.parameters.get("depth", 0.0))
                count = int(feature.parameters.get("count", 1))
                body.volume = max(0.0, body.volume - 3.141592653589793 * (diameter / 2.0) ** 2 * depth * count)
                body.face_count += count
            elif feature_type == FeatureType.THREAD:
                body.metadata["thread"] = dict(feature.parameters)
            elif feature_type == FeatureType.PATTERN:
                body = apply_pattern(body, feature.parameters)
            elif feature_type == FeatureType.MIRROR:
                factor = float(feature.parameters.get("factor", 2.0))
                body.volume *= factor
                body.face_count = int(body.face_count * factor)
                body.edge_count = int(body.edge_count * factor)
            elif feature_type == FeatureType.BOOLEAN_UNION:
                body = BooleanOperation.apply("union", body, feature.parameters["operand"])
            elif feature_type == FeatureType.BOOLEAN_SUBTRACT:
                body = BooleanOperation.apply("subtract", body, feature.parameters["operand"])
            elif feature_type == FeatureType.BOOLEAN_INTERSECT:
                body = BooleanOperation.apply("intersect", body, feature.parameters["operand"])
            elif feature_type == FeatureType.SPLIT_BODY:
                body.body_count = max(1, int(feature.parameters.get("segments", 2)))
            elif feature_type == FeatureType.COMBINE_BODIES:
                body.body_count = max(1, int(feature.parameters.get("count", 1)) - 1)
            elif feature_type == FeatureType.OFFSET_FACE:
                offset = float(feature.parameters.get("offset", 0.0))
                body.volume += abs(offset) * max(1, body.face_count)
            elif feature_type == FeatureType.REPLACE_FACE:
                body.face_count += int(feature.parameters.get("count", 1))
            elif feature_type == FeatureType.DELETE_FACE:
                body.face_count = max(1, body.face_count - int(feature.parameters.get("count", 1)))
            part.parametric_history.record({"feature": feature.name, "body": body.clone().metadata | {"volume": body.volume, "faces": body.face_count}})
            part.design_history.record(feature, body)
        part.set_primary_body(body)
        self.feature_tree.set_features(self._features)
        return RegenerationResult(converged=True, iterations=iterations, residual=0.0)

    def undo(self, part: "PartModel") -> bool:
        """Undo the last feature edit/create/suppress action."""
        if not self._undo_stack:
            return False
        self._redo_stack.append(self._serialize_state())
        self._restore_state(self._undo_stack.pop())
        self.regenerate(part)
        return True

    def redo(self, part: "PartModel") -> bool:
        """Redo the last undone feature action."""
        if not self._redo_stack:
            return False
        self._undo_stack.append(self._serialize_state())
        self._restore_state(self._redo_stack.pop())
        self.regenerate(part)
        return True

    def _get_feature(self, feature_id: str) -> Feature:
        for feature in self._features:
            if feature.feature_id == feature_id:
                return feature
        raise KeyError(f"Feature '{feature_id}' was not found")

    def _active_features(self) -> list[Feature]:
        if self._rollback_name is None:
            return list(self._features)
        visible: list[Feature] = []
        for feature in self._features:
            visible.append(feature)
            if feature.name == self._rollback_name:
                break
        return visible

    def _push_undo_state(self) -> None:
        self._undo_stack.append(self._serialize_state())
        self._redo_stack.clear()

    def _serialize_state(self) -> dict[str, Any]:
        return {
            "features": [
                {
                    "feature_id": feature.feature_id,
                    "name": feature.name,
                    "feature_type": feature.feature_type.value,
                    "parameters": deepcopy(feature.parameters),
                    "suppressed": feature.suppressed,
                    "dependencies": list(feature.dependencies),
                }
                for feature in self._features
            ],
            "rollback_name": self._rollback_name,
        }

    def _restore_state(self, state: dict[str, Any]) -> None:
        self._features = [
            Feature(
                feature_id=item["feature_id"],
                name=item["name"],
                feature_type=FeatureType(item["feature_type"]),
                parameters=deepcopy(item["parameters"]),
                suppressed=bool(item["suppressed"]),
                dependencies=tuple(item.get("dependencies", [])),
            )
            for item in state["features"]
        ]
        self._rollback_name = state.get("rollback_name")
        self.feature_tree.set_features(self._features)
