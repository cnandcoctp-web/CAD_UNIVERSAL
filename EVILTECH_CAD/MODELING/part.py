"""Part model container for the modeling engine."""

from __future__ import annotations

from dataclasses import dataclass, field

from GEOMETRY.point import Point3D
from MODELING.feature import DesignHistory, FeatureManager, FeatureTree, ModelBody, ParametricHistory, ReferenceGeometry, WorkAxis, WorkPlane, WorkPoint
from MODELING.sketch import SketchEnvironment, SketchManager


@dataclass(slots=True)
class PartModel:
    """A parametric part model containing sketches, features, and bodies."""

    name: str
    sketch_manager: SketchManager = field(default_factory=SketchManager)
    feature_manager: FeatureManager = field(default_factory=FeatureManager)
    _bodies: list[ModelBody] = field(default_factory=list, repr=False)
    parametric_history: ParametricHistory = field(default_factory=ParametricHistory)
    design_history: DesignHistory = field(default_factory=DesignHistory)
    feature_tree: FeatureTree = field(init=False)

    def __post_init__(self) -> None:
        self.feature_tree = self.feature_manager.feature_tree

    def default_environment(self) -> SketchEnvironment:
        """Return the default sketch environment for the part."""
        return SketchEnvironment(
            work_plane=WorkPlane(name="XY", origin=Point3D(0.0, 0.0, 0.0), normal=(0.0, 0.0, 1.0)),
            work_axis=WorkAxis(name="Z", direction=(0.0, 0.0, 1.0)),
            work_point=WorkPoint(name="Origin", point=Point3D(0.0, 0.0, 0.0)),
            references=[ReferenceGeometry(name="Origin Plane", geometry_type="plane")],
        )

    def primary_body(self) -> ModelBody:
        """Return the primary model body."""
        if not self._bodies:
            return ModelBody(name=f"{self.name}-empty", volume=0.0, face_count=0, edge_count=0, body_count=0)
        return self._bodies[0]

    def set_primary_body(self, body: ModelBody) -> None:
        """Replace the primary model body."""
        self._bodies = [body]
