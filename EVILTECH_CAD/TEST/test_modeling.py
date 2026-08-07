"""Regression and integration tests for the EvilTech CAD modeling engine."""

from __future__ import annotations

from pathlib import Path

import pytest

from GEOMETRY.point import Point3D
from MODELING.assembly import AssemblyManager, ComponentManager, Mate, PartManager
from MODELING.boolean import BooleanOperation
from MODELING.feature import FeatureType, ModelBody, ReferenceGeometry, WorkAxis, WorkPlane, WorkPoint
from MODELING.part import PartModel
from MODELING.sketch import SketchEnvironment, SketchManager, SketchProfile, SketchValidator


def build_profile(name: str, area: float = 20.0, perimeter: float = 18.0) -> SketchProfile:
    return SketchProfile(name=name, area=area, perimeter=perimeter, closed=True)


def test_sketch_manager_environment_and_validator() -> None:
    environment = SketchEnvironment(
        work_plane=WorkPlane(name="XY", origin=Point3D(0.0, 0.0, 0.0), normal=(0.0, 0.0, 1.0)),
        work_axis=WorkAxis(name="Z", direction=(0.0, 0.0, 1.0)),
        work_point=WorkPoint(name="Origin", point=Point3D(0.0, 0.0, 0.0)),
        references=[ReferenceGeometry(name="Base", geometry_type="plane")],
    )
    manager = SketchManager()
    profile = build_profile("base")
    sketch = manager.create_sketch("Sketch-1", environment, [profile])

    result = SketchValidator().validate(sketch)

    assert result.is_valid is True
    assert sketch.profile_count() == 1
    assert sketch.environment.work_plane.name == "XY"


def test_feature_manager_builds_parametric_body_and_rebuilds_on_edit() -> None:
    part = PartModel(name="Bracket")
    sketch = part.sketch_manager.create_sketch("Base Sketch", part.default_environment(), [build_profile("base", area=12.0, perimeter=14.0)])

    extrude = part.feature_manager.create_feature(FeatureType.EXTRUDE, "Extrude-1", {"sketch": sketch.name, "distance": 5.0})
    result = part.feature_manager.regenerate(part)

    assert result.converged is True
    assert part.primary_body().volume == pytest.approx(60.0)

    part.feature_manager.edit_feature(extrude.feature_id, distance=8.0)
    part.feature_manager.regenerate(part)
    assert part.primary_body().volume == pytest.approx(96.0)
    assert part.feature_tree.feature_names() == ["Extrude-1"]


def test_multiple_feature_operations_create_stable_history() -> None:
    part = PartModel(name="Housing")
    sketch = part.sketch_manager.create_sketch("Section", part.default_environment(), [build_profile("section", area=10.0, perimeter=16.0)])
    path = part.sketch_manager.create_sketch("Path", part.default_environment(), [build_profile("path", area=4.0, perimeter=10.0)])

    part.feature_manager.create_feature(FeatureType.EXTRUDE, "Extrude", {"sketch": sketch.name, "distance": 4.0})
    part.feature_manager.create_feature(FeatureType.SHELL, "Shell", {"thickness": 0.25})
    part.feature_manager.create_feature(FeatureType.HOLE, "Hole", {"diameter": 1.0, "depth": 2.0, "count": 2})
    part.feature_manager.create_feature(FeatureType.PATTERN, "Pattern", {"count": 3, "spacing": 5.0})
    part.feature_manager.create_feature(FeatureType.SWEEP, "Sweep", {"sketch": sketch.name, "path": path.name, "length": 6.0})
    result = part.feature_manager.regenerate(part)

    assert result.converged is True
    assert len(part.design_history.entries()) >= 5
    assert part.primary_body().volume > 0.0


def test_revolve_loft_rib_thread_draft_and_face_operations() -> None:
    part = PartModel(name="Valve")
    base = part.sketch_manager.create_sketch("Base", part.default_environment(), [build_profile("base", area=8.0, perimeter=12.0)])
    loft_a = part.sketch_manager.create_sketch("Loft-A", part.default_environment(), [build_profile("la", area=5.0, perimeter=10.0)])
    loft_b = part.sketch_manager.create_sketch("Loft-B", part.default_environment(), [build_profile("lb", area=7.0, perimeter=11.0)])
    part.feature_manager.create_feature(FeatureType.REVOLVE, "Revolve", {"sketch": base.name, "angle": 180.0, "radius": 2.0})
    part.feature_manager.create_feature(FeatureType.LOFT, "Loft", {"profiles": [loft_a.name, loft_b.name], "length": 5.0})
    part.feature_manager.create_feature(FeatureType.RIB, "Rib", {"thickness": 0.5, "length": 3.0})
    part.feature_manager.create_feature(FeatureType.THREAD, "Thread", {"pitch": 1.5, "length": 8.0})
    part.feature_manager.create_feature(FeatureType.DRAFT, "Draft", {"angle": 2.0})
    part.feature_manager.create_feature(FeatureType.OFFSET_FACE, "Offset Face", {"offset": 0.2})
    part.feature_manager.create_feature(FeatureType.REPLACE_FACE, "Replace Face", {"count": 1})
    part.feature_manager.create_feature(FeatureType.DELETE_FACE, "Delete Face", {"count": 1})
    result = part.feature_manager.regenerate(part)

    assert result.converged is True
    assert part.primary_body().face_count > 0
    assert part.design_history.entries()[-1]["feature"] == "Delete Face"


def test_boolean_mirror_split_combine_and_regeneration_controls() -> None:
    part = PartModel(name="Frame")
    sketch = part.sketch_manager.create_sketch("Body", part.default_environment(), [build_profile("body", area=15.0, perimeter=20.0)])
    part.feature_manager.create_feature(FeatureType.EXTRUDE, "Body", {"sketch": sketch.name, "distance": 4.0})
    part.feature_manager.create_feature(FeatureType.MIRROR, "Mirror", {"factor": 2.0})
    part.feature_manager.create_feature(FeatureType.SPLIT_BODY, "Split", {"segments": 2})
    part.feature_manager.create_feature(FeatureType.COMBINE_BODIES, "Combine", {"count": 2})
    part.feature_manager.create_feature(FeatureType.BOOLEAN_UNION, "Union", {"operand": ModelBody(name="operand", volume=10.0, face_count=6, edge_count=12, body_count=1)})
    result = part.feature_manager.regenerate(part)

    assert result.converged is True
    feature = part.feature_manager.feature_tree.find_by_name("Mirror")
    part.feature_manager.suppress_feature(feature.feature_id, suppressed=True)
    part.feature_manager.regenerate(part)
    suppressed_volume = part.primary_body().volume
    part.feature_manager.suppress_feature(feature.feature_id, suppressed=False)
    part.feature_manager.regenerate(part)
    assert part.primary_body().volume >= suppressed_volume
    assert part.feature_manager.rollback_to("Split") is True


def test_undo_redo_and_parameter_driven_rebuild() -> None:
    part = PartModel(name="Plate")
    sketch = part.sketch_manager.create_sketch("Plate Sketch", part.default_environment(), [build_profile("plate", area=9.0, perimeter=12.0)])
    feature = part.feature_manager.create_feature(FeatureType.EXTRUDE, "Plate Extrude", {"sketch": sketch.name, "distance": 2.0})
    part.feature_manager.regenerate(part)
    volume_before = part.primary_body().volume

    part.feature_manager.edit_feature(feature.feature_id, distance=6.0)
    part.feature_manager.regenerate(part)
    assert part.primary_body().volume > volume_before

    assert part.feature_manager.undo(part) is True
    assert part.primary_body().volume == pytest.approx(volume_before)
    assert part.feature_manager.redo(part) is True
    assert part.primary_body().volume == pytest.approx(54.0)


def test_assembly_managers_components_mates_and_exploded_views() -> None:
    part_manager = PartManager()
    component_manager = ComponentManager()
    assembly_manager = AssemblyManager(component_manager=component_manager)
    base = PartModel(name="Base")
    cap = PartModel(name="Cap")
    part_manager.register(base)
    part_manager.register(cap)
    component_manager.add_component("base-1", base)
    component_manager.add_component("cap-1", cap)
    assembly = assembly_manager.create_assembly("Valve Assembly")
    assembly_manager.add_to_assembly(assembly.name, "base-1")
    assembly_manager.add_to_assembly(assembly.name, "cap-1")
    assembly_manager.add_mate(assembly.name, Mate(name="Mate-1", first_component="base-1", second_component="cap-1", mate_type="concentric"))
    exploded = assembly_manager.create_exploded_view(assembly.name, {"cap-1": (0.0, 0.0, 10.0)})

    assert assembly.component_count() == 2
    assert assembly.assembly_tree.node_names() == ["base-1", "cap-1"]
    assert len(assembly.mates) == 1
    assert exploded.offsets["cap-1"] == (0.0, 0.0, 10.0)


def test_boolean_operations_and_feature_history_integration() -> None:
    part = PartModel(name="Boolean Part")
    body = ModelBody(name="primary", volume=50.0, face_count=10, edge_count=20, body_count=1)
    operand = ModelBody(name="operand", volume=12.0, face_count=6, edge_count=12, body_count=1)

    union = BooleanOperation.apply("union", body, operand)
    subtract = BooleanOperation.apply("subtract", union, operand)
    intersect = BooleanOperation.apply("intersect", union, operand)

    assert union.volume == pytest.approx(62.0)
    assert subtract.volume == pytest.approx(50.0)
    assert intersect.volume == pytest.approx(12.0)


def test_modeling_stress_regeneration_and_persistence_like_history() -> None:
    part = PartModel(name="Stress Part")
    profile = part.sketch_manager.create_sketch("Stress Sketch", part.default_environment(), [build_profile("stress", area=6.0, perimeter=10.0)])
    for index in range(20):
        part.feature_manager.create_feature(FeatureType.EXTRUDE, f"Extrude-{index}", {"sketch": profile.name, "distance": 1.0 + index * 0.1})
    result = part.feature_manager.regenerate(part)

    assert result.converged is True
    assert result.iterations <= 40
    assert part.feature_tree.feature_count() == 20
    assert len(part.parametric_history.snapshots()) >= 20
