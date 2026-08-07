"""Constraint management, solving, history, dependency, and persistence."""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from time import perf_counter
from typing import Any

from CONSTRAINTS.constraint_registry import Constraint, ConstraintEvent, ConstraintRegistry, ConstraintType
from CONSTRAINTS.dimensional_constraints import apply_dimensional, evaluate_dimensional
from CONSTRAINTS.geometric_constraints import apply_geometric, evaluate_geometric
from CONSTRAINTS.tolerance_constraints import ConstraintTolerance, ConstraintValidationResult, ConstraintValidator
from GEOMETRY.circle import Circle
from GEOMETRY.line import Line
from GEOMETRY.point import Point3D
from CORE.resource_manager import ResourceManager


@dataclass(slots=True)
class SolveResult:
    """Result of a constraint-solver pass."""

    converged: bool
    iterations: int
    residual: float
    conflicts: list[str] = field(default_factory=list)
    cycles: list[list[str]] = field(default_factory=list)
    elapsed_seconds: float = 0.0


class ConstraintDependencyGraph:
    """Directed dependency graph between constraints."""

    def __init__(self) -> None:
        self._edges: dict[str, set[str]] = {}

    def rebuild(self, constraints: list[Constraint]) -> None:
        """Rebuild the graph from a list of constraints."""
        self._edges = {constraint.constraint_id: set(constraint.dependencies) for constraint in constraints}

    def detect_cycles(self) -> list[list[str]]:
        """Return detected dependency cycles."""
        visited: set[str] = set()
        active: set[str] = set()
        path: list[str] = []
        cycles: list[list[str]] = []

        def visit(node: str) -> None:
            if node in active:
                index = path.index(node)
                cycles.append(path[index:] + [node])
                return
            if node in visited:
                return
            visited.add(node)
            active.add(node)
            path.append(node)
            for dependency in self._edges.get(node, set()):
                if dependency in self._edges:
                    visit(dependency)
            path.pop()
            active.remove(node)

        for node in self._edges:
            visit(node)
        return cycles


class ConstraintHistory:
    """Undo and redo snapshots for the constraint manager."""

    def __init__(self) -> None:
        self._undo_stack: list[dict[str, Any]] = []
        self._redo_stack: list[dict[str, Any]] = []

    def push_undo(self, state: dict[str, Any]) -> None:
        """Push a state snapshot to the undo stack."""
        self._undo_stack.append(deepcopy(state))
        self._redo_stack.clear()

    def undo(self, current_state: dict[str, Any]) -> dict[str, Any] | None:
        """Return the previous state and push the current one onto redo."""
        if not self._undo_stack:
            return None
        self._redo_stack.append(deepcopy(current_state))
        return self._undo_stack.pop()

    def redo(self, current_state: dict[str, Any]) -> dict[str, Any] | None:
        """Return the next redo state and push the current one onto undo."""
        if not self._redo_stack:
            return None
        self._undo_stack.append(deepcopy(current_state))
        return self._redo_stack.pop()


class ConstraintPersistence:
    """Persist constraint-manager state to and from JSON."""

    def save(self, manager: "ConstraintManager", path: Path) -> Path:
        """Persist the full constraint-manager state."""
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8") as handle:
            json.dump(manager.serialize_state(), handle, indent=2, sort_keys=True)
        return target

    def load(self, path: Path) -> "ConstraintManager":
        """Load a persisted constraint-manager state."""
        source = Path(path)
        with source.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        manager = ConstraintManager()
        manager.restore_state(payload)
        return manager


class ConstraintSolver:
    """Iterative, numerically stable solver for supported constraint types."""

    def __init__(self, tolerance: ConstraintTolerance | None = None, max_iterations: int = 250) -> None:
        self.tolerance = tolerance or ConstraintTolerance()
        self.max_iterations = max_iterations

    def solve(self, manager: "ConstraintManager", dirty_entity_ids: set[str] | None = None) -> SolveResult:
        """Solve all relevant constraints and return convergence information."""
        start = perf_counter()
        relevant = manager.relevant_constraints(dirty_entity_ids)
        conflicts = manager.validator.detect_conflicts(relevant, manager.entities)
        manager.dependency_graph.rebuild(relevant)
        cycles = manager.dependency_graph.detect_cycles()
        if conflicts or cycles:
            return SolveResult(converged=False, iterations=0, residual=float("inf"), conflicts=conflicts, cycles=cycles, elapsed_seconds=perf_counter() - start)

        residual = 0.0
        convergence_threshold = self._convergence_threshold(relevant)
        for iteration in range(1, self.max_iterations + 1):
            residual = 0.0
            for constraint in relevant:
                if not constraint.active:
                    continue
                if constraint.mode in {"reference", "driven"} or constraint.constraint_type in {ConstraintType.REFERENCE, ConstraintType.DRIVEN, ConstraintType.DRIVING}:
                    residual = max(residual, self._evaluate(constraint, manager.entities))
                    continue
                current = self._evaluate(constraint, manager.entities)
                residual = max(residual, current)
                if current > self._tolerance_for(constraint):
                    updated = self._apply(constraint, manager.entities)
                    residual = max(residual, updated)
            if residual <= convergence_threshold:
                return SolveResult(converged=True, iterations=iteration, residual=residual, elapsed_seconds=perf_counter() - start)
        return SolveResult(converged=False, iterations=self.max_iterations, residual=residual, elapsed_seconds=perf_counter() - start)

    def _tolerance_for(self, constraint: Constraint) -> float:
        if constraint.constraint_type == ConstraintType.ANGLE:
            return self.tolerance.angular
        return self.tolerance.linear

    def _convergence_threshold(self, constraints: list[Constraint]) -> float:
        """Return the active convergence threshold for the solve pass."""
        if len(constraints) >= 20:
            return max(self.tolerance.linear, 1e-3)
        return self.tolerance.linear

    def _evaluate(self, constraint: Constraint, entities: dict[str, object]) -> float:
        if constraint.constraint_type in {ConstraintType.DISTANCE, ConstraintType.ANGLE, ConstraintType.RADIUS, ConstraintType.DIAMETER}:
            return evaluate_dimensional(constraint, entities, self.tolerance)
        return evaluate_geometric(constraint, entities, self.tolerance)

    def _apply(self, constraint: Constraint, entities: dict[str, object]) -> float:
        if constraint.constraint_type in {ConstraintType.DISTANCE, ConstraintType.ANGLE, ConstraintType.RADIUS, ConstraintType.DIAMETER}:
            return apply_dimensional(constraint, entities, self.tolerance)
        return apply_geometric(constraint, entities, self.tolerance)


class ConstraintManager:
    """Own entities, constraints, events, persistence, and solving operations."""

    def __init__(self) -> None:
        self.registry = ConstraintRegistry()
        self.validator = ConstraintValidator()
        self.solver = ConstraintSolver(self.validator.tolerance)
        self.persistence = ConstraintPersistence()
        self.dependency_graph = ConstraintDependencyGraph()
        self.history = ConstraintHistory()
        self.resource_manager = ResourceManager()
        self.entities: dict[str, object] = {}
        self.constraints: dict[str, Constraint] = {}
        self.events: list[ConstraintEvent] = []

    def add_entity(self, entity_id: str, entity: object) -> None:
        """Register a named geometry entity for constraint solving."""
        if not entity_id:
            raise ValueError("entity_id must be non-empty")
        self.history.push_undo(self.serialize_state())
        self.entities[entity_id] = entity
        self._register_resource(f"constraint-entity:{entity_id}", entity)
        self.events.append(ConstraintEvent("entity_added", entity_id))

    def add_constraint(
        self,
        constraint_type: ConstraintType | str,
        entity_ids: tuple[str, ...],
        value: float | None = None,
        metadata: dict[str, Any] | None = None,
        dependencies: tuple[str, ...] | None = None,
        mode: str = "driving",
    ) -> Constraint:
        """Create and register a new constraint."""
        prepared_metadata = dict(metadata or {})
        if ConstraintType(constraint_type) == ConstraintType.LOCK and "locked_state" not in prepared_metadata:
            locked_entity = self.entities[entity_ids[0]]
            prepared_metadata["locked_state"] = self._serialize_entity(locked_entity)
        self.history.push_undo(self.serialize_state())
        constraint = self.registry.create_constraint(constraint_type, entity_ids, value=value, metadata=prepared_metadata, dependencies=dependencies, mode=mode)
        self.constraints[constraint.constraint_id] = constraint
        self.events.append(ConstraintEvent("constraint_added", constraint.constraint_id))
        self._register_resource(f"constraint:{constraint.constraint_id}", constraint.to_dict())
        return constraint

    def remove_constraint(self, constraint_id: str) -> None:
        """Remove a constraint by identifier."""
        if constraint_id not in self.constraints:
            raise KeyError(f"Constraint '{constraint_id}' was not found")
        self.history.push_undo(self.serialize_state())
        del self.constraints[constraint_id]
        self.resource_manager.release_resource(f"constraint:{constraint_id}")
        self.events.append(ConstraintEvent("constraint_removed", constraint_id))

    def edit_constraint(self, constraint_id: str, **updates: Any) -> Constraint:
        """Edit a constraint in place and return it."""
        if constraint_id not in self.constraints:
            raise KeyError(f"Constraint '{constraint_id}' was not found")
        self.history.push_undo(self.serialize_state())
        constraint = self.constraints[constraint_id]
        for key, value in updates.items():
            if not hasattr(constraint, key):
                raise AttributeError(f"Constraint has no attribute '{key}'")
            setattr(constraint, key, value)
        self.events.append(ConstraintEvent("constraint_edited", constraint_id))
        return constraint

    def validate(self) -> ConstraintValidationResult:
        """Validate all constraints and return the aggregate result."""
        errors: list[str] = []
        warnings: list[str] = []
        constraints = list(self.constraints.values())
        for constraint in constraints:
            result = self.validator.validate_constraint(constraint, self.entities)
            errors.extend(result.errors)
            warnings.extend(result.warnings)
        errors.extend(self.validator.detect_conflicts(constraints, self.entities))
        self.dependency_graph.rebuild(constraints)
        cycles = self.dependency_graph.detect_cycles()
        if cycles:
            errors.extend([f"Dependency cycle detected: {' -> '.join(cycle)}" for cycle in cycles])
        return ConstraintValidationResult(is_valid=not errors, errors=errors, warnings=warnings)

    def resolve_conflicts(self) -> list[str]:
        """Resolve simple conflicting dimensional constraints using last-write-wins."""
        disabled: list[str] = []
        seen: dict[tuple[str, tuple[str, ...]], str] = {}
        for constraint in list(self.constraints.values()):
            if constraint.constraint_type not in {ConstraintType.DISTANCE, ConstraintType.ANGLE, ConstraintType.RADIUS, ConstraintType.DIAMETER, ConstraintType.OFFSET}:
                continue
            key = (constraint.constraint_type.value, tuple(sorted(constraint.entity_ids)))
            if key in seen:
                older = self.constraints[seen[key]]
                older.active = False
                disabled.append(older.constraint_id)
            seen[key] = constraint.constraint_id
        if disabled:
            self.events.append(ConstraintEvent("conflicts_resolved", ",".join(disabled)))
        return disabled

    def solve(self, dirty_entity_ids: set[str] | None = None) -> SolveResult:
        """Solve all active constraints or the relevant incremental subset."""
        self.history.push_undo(self.serialize_state())
        result = self.solver.solve(self, dirty_entity_ids=dirty_entity_ids)
        self.events.append(ConstraintEvent("solved", f"converged={result.converged};iterations={result.iterations}"))
        return result

    def relevant_constraints(self, dirty_entity_ids: set[str] | None = None) -> list[Constraint]:
        """Return constraints relevant to the full or incremental solve request."""
        if not dirty_entity_ids:
            return list(self.constraints.values())
        return [constraint for constraint in self.constraints.values() if set(constraint.entity_ids).intersection(dirty_entity_ids)]

    def undo(self) -> bool:
        """Undo the last mutating operation."""
        state = self.history.undo(self.serialize_state())
        if state is None:
            return False
        self.restore_state(state)
        self.events.append(ConstraintEvent("undo", "state_restored"))
        return True

    def redo(self) -> bool:
        """Redo the last undone operation."""
        state = self.history.redo(self.serialize_state())
        if state is None:
            return False
        self.restore_state(state)
        self.events.append(ConstraintEvent("redo", "state_restored"))
        return True

    def serialize_state(self) -> dict[str, Any]:
        """Serialize entities, constraints, and events."""
        return {
            "entities": {entity_id: self._serialize_entity(entity) for entity_id, entity in self.entities.items()},
            "constraints": [constraint.to_dict() for constraint in self.constraints.values()],
            "events": [{"event_type": event.event_type, "detail": event.detail, "timestamp": event.timestamp} for event in self.events],
        }

    def restore_state(self, payload: dict[str, Any]) -> None:
        """Restore entities, constraints, and events from a serialized state."""
        self.entities = {entity_id: self._deserialize_entity(entity_payload) for entity_id, entity_payload in payload.get("entities", {}).items()}
        self.constraints = {}
        for item in payload.get("constraints", []):
            constraint = Constraint.from_dict(item)
            self.constraints[constraint.constraint_id] = constraint
        self.events = [ConstraintEvent(event_type=item["event_type"], detail=item["detail"], timestamp=item["timestamp"]) for item in payload.get("events", [])]
        self.resource_manager = ResourceManager()
        for entity_id, entity in self.entities.items():
            self._register_resource(f"constraint-entity:{entity_id}", entity)
        for constraint in self.constraints.values():
            self._register_resource(f"constraint:{constraint.constraint_id}", constraint.to_dict())

    def save(self, path: Path) -> Path:
        """Persist the full manager state to disk."""
        return self.persistence.save(self, path)

    @classmethod
    def load(cls, path: Path) -> "ConstraintManager":
        """Load a manager state from disk."""
        return ConstraintPersistence().load(path)

    def _register_resource(self, name: str, value: object) -> None:
        try:
            self.resource_manager.release_resource(name)
        except Exception:
            pass
        self.resource_manager.register_resource(name, value)

    @staticmethod
    def _serialize_entity(entity: object) -> dict[str, Any]:
        if isinstance(entity, Point3D):
            return {"type": "Point3D", "x": entity.x, "y": entity.y, "z": entity.z}
        if isinstance(entity, Line):
            return {
                "type": "Line",
                "start": ConstraintManager._serialize_entity(entity.start),
                "end": ConstraintManager._serialize_entity(entity.end),
            }
        if isinstance(entity, Circle):
            return {
                "type": "Circle",
                "center": ConstraintManager._serialize_entity(entity.center),
                "radius": entity.radius,
            }
        raise TypeError(f"Unsupported entity type '{entity.__class__.__name__}'")

    @staticmethod
    def _deserialize_entity(payload: dict[str, Any]) -> object:
        entity_type = payload["type"]
        if entity_type == "Point3D":
            return Point3D(payload["x"], payload["y"], payload.get("z", 0.0))
        if entity_type == "Line":
            return Line(
                ConstraintManager._deserialize_entity(payload["start"]),
                ConstraintManager._deserialize_entity(payload["end"]),
            )
        if entity_type == "Circle":
            return Circle(
                ConstraintManager._deserialize_entity(payload["center"]),
                payload["radius"],
            )
        raise ValueError(f"Unsupported serialized entity type '{entity_type}'")
