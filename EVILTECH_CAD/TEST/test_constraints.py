"""Regression, accuracy, integration, and stress tests for the constraint engine."""

from __future__ import annotations

from pathlib import Path

import pytest

from CONSTRAINTS.constraint_registry import ConstraintType
from CONSTRAINTS.constraint_solver import ConstraintManager
from GEOMETRY.circle import Circle
from GEOMETRY.line import Line
from GEOMETRY.point import Point3D


def build_manager() -> ConstraintManager:
    manager = ConstraintManager()
    manager.add_entity("p0", Point3D(0.0, 0.0, 0.0))
    manager.add_entity("p1", Point3D(4.0, 3.0, 0.0))
    manager.add_entity("p2", Point3D(2.0, 1.0, 0.0))
    manager.add_entity("axis", Point3D(0.0, 0.0, 0.0))
    manager.add_entity("line_a", Line(Point3D(0.0, 0.0, 0.0), Point3D(5.0, 0.0, 0.0)))
    manager.add_entity("line_b", Line(Point3D(1.0, 1.0, 0.0), Point3D(4.0, 3.0, 0.0)))
    manager.add_entity("circle_a", Circle(Point3D(0.0, 5.0, 0.0), 2.0))
    manager.add_entity("circle_b", Circle(Point3D(2.0, 6.0, 0.0), 1.0))
    return manager


def test_registry_exposes_all_supported_constraint_types() -> None:
    manager = ConstraintManager()

    supported = {constraint_type.value for constraint_type in manager.registry.supported_types()}

    assert supported == {
        "coincident",
        "parallel",
        "perpendicular",
        "horizontal",
        "vertical",
        "distance",
        "angle",
        "radius",
        "diameter",
        "concentric",
        "tangent",
        "equal_length",
        "equal_radius",
        "symmetry",
        "midpoint",
        "offset",
        "lock",
        "reference",
        "driving",
        "driven",
    }


def test_solver_applies_basic_constraints_and_updates_geometry() -> None:
    manager = build_manager()
    manager.add_constraint(ConstraintType.HORIZONTAL, ("line_b",))
    manager.add_constraint(ConstraintType.DISTANCE, ("p0", "p1"), value=10.0)
    manager.add_constraint(ConstraintType.MIDPOINT, ("p2", "p0", "p1"))

    result = manager.solve()

    assert result.converged is True
    assert manager.entities["line_b"].start.y == pytest.approx(manager.entities["line_b"].end.y)
    assert manager.entities["p0"].distance_to(manager.entities["p1"]) == pytest.approx(10.0, rel=1e-5)
    assert manager.entities["p2"].x == pytest.approx((manager.entities["p0"].x + manager.entities["p1"].x) / 2.0)


def test_solver_applies_relational_and_dimensional_constraints() -> None:
    manager = build_manager()
    manager.add_constraint(ConstraintType.PERPENDICULAR, ("line_a", "line_b"))
    manager.add_constraint(ConstraintType.EQUAL_LENGTH, ("line_a", "line_b"))
    manager.add_constraint(ConstraintType.CONCENTRIC, ("circle_a", "circle_b"))
    manager.add_constraint(ConstraintType.EQUAL_RADIUS, ("circle_a", "circle_b"))
    manager.add_constraint(ConstraintType.TANGENT, ("line_a", "circle_a"))
    manager.add_constraint(ConstraintType.RADIUS, ("circle_a",), value=2.5)
    manager.add_constraint(ConstraintType.DIAMETER, ("circle_b",), value=5.0)

    result = manager.solve()

    assert result.converged is True
    assert abs(manager.entities["line_b"].end.x - manager.entities["line_b"].start.x) == pytest.approx(0.0, abs=1e-5)
    assert manager.entities["line_b"].length() == pytest.approx(manager.entities["line_a"].length(), rel=1e-5)
    assert manager.entities["circle_a"].center.x == pytest.approx(manager.entities["circle_b"].center.x)
    assert manager.entities["circle_a"].radius == pytest.approx(2.5)
    assert manager.entities["circle_b"].radius == pytest.approx(2.5)


def test_validator_detects_conflicts_and_dependency_cycles() -> None:
    manager = build_manager()
    first = manager.add_constraint(ConstraintType.DISTANCE, ("p0", "p1"), value=5.0)
    second = manager.add_constraint(ConstraintType.DISTANCE, ("p0", "p1"), value=7.0, dependencies=(first.constraint_id,))
    manager.edit_constraint(first.constraint_id, dependencies=(second.constraint_id,))

    validation = manager.validate()
    result = manager.solve()

    assert validation.is_valid is False
    assert any("Conflicting values" in error for error in validation.errors)
    assert any("Dependency cycle" in error for error in validation.errors)
    assert result.converged is False
    assert result.cycles


def test_conflict_resolution_undo_redo_and_incremental_solving() -> None:
    manager = build_manager()
    first = manager.add_constraint(ConstraintType.DISTANCE, ("p0", "p1"), value=5.0)
    second = manager.add_constraint(ConstraintType.DISTANCE, ("p0", "p1"), value=8.0)

    disabled = manager.resolve_conflicts()
    manager.solve(dirty_entity_ids={"p0", "p1"})

    assert first.constraint_id in disabled
    assert manager.entities["p0"].distance_to(manager.entities["p1"]) == pytest.approx(8.0, rel=1e-5)

    manager.edit_constraint(second.constraint_id, value=6.0)
    manager.solve(dirty_entity_ids={"p0", "p1"})
    assert manager.entities["p0"].distance_to(manager.entities["p1"]) == pytest.approx(6.0, rel=1e-5)

    assert manager.undo() is True
    assert manager.redo() is True


def test_lock_reference_driven_and_history_events() -> None:
    manager = build_manager()
    manager.add_constraint(ConstraintType.LOCK, ("p0",))
    manager.add_constraint(ConstraintType.REFERENCE, ("line_a",), mode="reference")
    manager.add_constraint(ConstraintType.DRIVEN, ("line_b",), mode="driven")
    manager.entities["p0"].x = 10.0
    manager.entities["p0"].y = 10.0

    result = manager.solve()

    assert result.converged is True
    assert manager.entities["p0"].x == pytest.approx(0.0)
    assert manager.entities["p0"].y == pytest.approx(0.0)
    assert any(event.event_type == "solved" for event in manager.events)


def test_constraint_persistence_saves_and_loads_manager_state(tmp_path: Path) -> None:
    manager = build_manager()
    manager.add_constraint(ConstraintType.HORIZONTAL, ("line_b",))
    manager.add_constraint(ConstraintType.DISTANCE, ("p0", "p1"), value=9.0)
    manager.solve()

    path = manager.save(tmp_path / "constraints.json")
    restored = ConstraintManager.load(path)

    assert len(restored.constraints) == 2
    assert restored.entities["p0"].distance_to(restored.entities["p1"]) == pytest.approx(9.0, rel=1e-5)


def test_large_sketch_stress_and_stability() -> None:
    manager = ConstraintManager()
    count = 25
    for index in range(count):
        manager.add_entity(f"p{index}", Point3D(float(index), 0.0 if index == 0 else 1.0, 0.0))
    for index in range(count - 1):
        manager.add_constraint(ConstraintType.DISTANCE, (f"p{index}", f"p{index + 1}"), value=5.0)
    for index in range(count - 1):
        manager.add_entity(f"l{index}", Line(manager.entities[f"p{index}"], manager.entities[f"p{index + 1}"]))
        manager.add_constraint(ConstraintType.HORIZONTAL, (f"l{index}",))

    result = manager.solve()

    assert result.converged is True
    assert result.iterations <= 250
    assert result.elapsed_seconds < 2.0
    for index in range(count - 1):
        assert manager.entities[f"p{index}"].distance_to(manager.entities[f"p{index + 1}"]) == pytest.approx(5.0, rel=1e-4)
        assert manager.entities[f"l{index}"].start.y == pytest.approx(manager.entities[f"l{index}"].end.y, abs=1e-3)
