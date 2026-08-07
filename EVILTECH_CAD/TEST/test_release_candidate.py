"""Release-candidate validation for the integrated EvilTech CAD system."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter
import tracemalloc

import pytest

from AI.engineering_assistant import EngineeringAssistant
from CONSTRAINTS.constraint_registry import ConstraintType
from CONSTRAINTS.constraint_solver import ConstraintManager
from ENGINEERING.engineering_manager import EngineeringManager
from ENGINEERING.engineering_models import DisciplineType
from GEOMETRY.circle import Circle
from GEOMETRY.line import Line
from GEOMETRY.point import Point3D
from GEOMETRY.vector import Vector3D
from IO.file_manager import ProjectManager
from MODELING.feature import FeatureType
from MODELING.part import PartModel
from MODELING.sketch import SketchProfile
from RENDERING.camera import OrthographicCamera
from RENDERING.renderer import RenderContext, RenderPipeline, Renderer
from RENDERING.scene import RenderObject, SceneGraph, SceneManager
from RENDERING.viewport import Viewport, ViewportManager
from SIMULATION.simulation_jobs import SimulationJobConfig, SimulationType
from SIMULATION.simulation_manager import SimulationManager


def build_part(name: str, feature_count: int) -> PartModel:
    """Build a deterministic part suitable for release validation."""
    part = PartModel(name=name)
    sketch = part.sketch_manager.create_sketch(
        "Base",
        part.default_environment(),
        [SketchProfile(name="base", area=18.0, perimeter=22.0)],
    )
    for index in range(feature_count):
        part.feature_manager.create_feature(
            FeatureType.EXTRUDE,
            f"Extrude-{index}",
            {"sketch": sketch.name, "distance": 2.0 + index * 0.25},
        )
    part.feature_manager.regenerate(part)
    return part


def build_constraints() -> ConstraintManager:
    """Create a solved constraint set for the release workflow."""
    manager = ConstraintManager()
    manager.add_entity("p0", Point3D(0.0, 0.0, 0.0))
    manager.add_entity("p1", Point3D(4.0, 3.0, 0.0))
    manager.add_entity("p2", Point3D(2.0, 1.0, 0.0))
    manager.add_entity("line-a", Line(Point3D(0.0, 0.0, 0.0), Point3D(5.0, 1.0, 0.0)))
    manager.add_constraint(ConstraintType.DISTANCE, ("p0", "p1"), value=10.0)
    manager.add_constraint(ConstraintType.MIDPOINT, ("p2", "p0", "p1"))
    manager.add_constraint(ConstraintType.HORIZONTAL, ("line-a",))
    result = manager.solve()
    assert result.converged is True
    return manager


def build_renderer() -> Renderer:
    """Create a headless renderer for the release workflow."""
    scene = SceneGraph(name="rc1")
    scene.add_object(RenderObject(identifier="line-1", geometry=Line(Point3D(0.0, 0.0, 0.0), Point3D(8.0, 0.0, 0.0))))
    scene.add_object(RenderObject(identifier="circle-1", geometry=Circle(Point3D(2.0, 2.0, 0.0), 1.5), show_bounds=True))
    return Renderer(
        context=RenderContext(workspace_mode="2D"),
        scene_manager=SceneManager(scene),
        viewport_manager=ViewportManager([Viewport(identifier="release", width=1280, height=720)]),
        pipeline=RenderPipeline(),
    )


def test_rc1_end_to_end_engineering_workflow(tmp_path: Path) -> None:
    project_manager = ProjectManager()
    snapshot = project_manager.create_new_project("RC1 Workflow", tmp_path / "rc1_workflow")
    part = build_part(name="RC1 Part", feature_count=12)
    constraints = build_constraints()
    renderer = build_renderer()
    camera = OrthographicCamera(
        position=Point3D(0.0, 0.0, 10.0),
        target=Point3D(0.0, 0.0, 0.0),
        up=Vector3D(0.0, 1.0, 0.0),
        width=20.0,
        height=12.0,
    )
    frame = renderer.render(camera=camera)

    snapshot.properties.update({
        "workflow": "rc1",
        "constraint_count": len(constraints.constraints),
        "renderable_count": len(frame["renderables"]),
    })
    snapshot.materials = ["Aluminum 6061", "Steel A36"]
    snapshot.asset_registry.register_asset("workflow-part", "assets/workflow_part.step")
    project_manager.save_project(snapshot)
    reopened = project_manager.open_project(snapshot.project_path)

    assistant = EngineeringAssistant()
    review = assistant.review_part(
        part,
        user_message="Validate the integrated engineering workflow for release readiness.",
        discipline="mechanical_engineering",
        project_snapshot=reopened,
        constraints=constraints,
    )

    engineering = EngineeringManager(storage_root=tmp_path / "engineering_runtime")
    calculation = engineering.run_calculation(
        engineering.create_calculation_request(
            discipline=DisciplineType.MECHANICAL_ENGINEERING,
            calculation_name="beam_bending_stress",
            inputs={"moment_nm": 1200.0, "section_modulus_mm3": 60000.0},
        )
    )
    report = engineering.report_generator.generate(
        reopened.metadata.project_id,
        engineering.sample_project_generator.generate(reopened, DisciplineType.MECHANICAL_ENGINEERING),
        calculation,
    )

    simulation = SimulationManager(storage_root=tmp_path / "simulation_runtime", max_workers=2)
    try:
        request = engineering.simulation_integration.build_request(
            discipline=DisciplineType.THERMODYNAMICS,
            simulation_type=SimulationType.THERMAL_ANALYSIS,
            parameters={"boundary_case": "steady_state", "step_delay": 0.001},
        )
        job = simulation.create_job(request.to_job_config(name="RC1 Thermal Check", total_steps=12))
        simulation.start_job(job.job_id)
        simulation.wait_for_job(job.job_id)
        simulation_result = simulation.results_database.get(job.job_id)
    finally:
        simulation.shutdown()

    assert reopened.metadata.project_id == snapshot.metadata.project_id
    assert reopened.properties["constraint_count"] == 3
    assert len(frame["renderables"]) == 2
    assert review["response"]["validated"] is True
    assert review["report"]["project_id"] == reopened.metadata.project_id
    assert calculation.value == pytest.approx(20.0, rel=1e-5)
    assert report["calculation"]["value"] == pytest.approx(20.0, rel=1e-5)
    assert simulation_result.status == "completed"


def test_rc1_performance_and_memory_benchmarks(tmp_path: Path) -> None:
    part = build_part(name="RC1 Performance Part", feature_count=18)
    assistant = EngineeringAssistant()
    engineering = EngineeringManager(storage_root=tmp_path / "engineering_runtime")

    tracemalloc.start()
    started = perf_counter()
    review = assistant.review_part(
        part,
        user_message="Benchmark RC1 performance and memory characteristics.",
        discipline="manufacturing",
    )
    result = engineering.run_calculation(
        engineering.create_calculation_request(
            discipline=DisciplineType.ORBITAL_MECHANICS,
            calculation_name="orbital_velocity",
            inputs={"gravitational_parameter": 398600.4418, "radius_km": 7000.0},
        )
    )
    elapsed = perf_counter() - started
    current_bytes, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    assert review["response"]["validated"] is True
    assert result.value == pytest.approx(7.546053, rel=1e-4)
    assert elapsed < 5.0
    assert current_bytes >= 0
    assert peak_bytes < 128 * 1024 * 1024


def test_rc1_large_project_save_reload_and_analysis(tmp_path: Path) -> None:
    project_manager = ProjectManager()
    snapshot = project_manager.create_new_project("RC1 Large Project", tmp_path / "rc1_large_project")
    part = build_part(name="Large RC1 Part", feature_count=30)
    for index in range(25):
        snapshot.asset_registry.register_asset(f"asset-{index}", f"assets/asset_{index}.step")
    snapshot.properties["assemblies"] = 4
    snapshot.properties["parts"] = 25
    snapshot.materials = ["Aluminum 6061", "Steel A36", "ABS"]
    project_manager.save_project(snapshot)
    reopened = project_manager.open_project(snapshot.project_path)

    review = EngineeringAssistant().review_part(
        part,
        user_message="Review this larger integrated project for RC1 readiness.",
        discipline="architecture",
        project_snapshot=reopened,
    )

    assert len(reopened.asset_registry.to_dict()) == 25
    assert reopened.properties["parts"] == 25
    assert review["report"]["project_id"] == reopened.metadata.project_id
    assert review["response"]["recommendations"]


def test_rc1_long_running_simulation_stability(tmp_path: Path) -> None:
    simulation = SimulationManager(storage_root=tmp_path / "rc1_long_sim", max_workers=2)
    try:
        job = simulation.create_job(
            SimulationJobConfig(
                name="RC1 Long Simulation",
                simulation_type=SimulationType.FATIGUE_ANALYSIS,
                total_steps=90,
                parameters={"step_delay": 0.001, "discipline": "mechanical_engineering"},
                checkpoint_interval=9,
            )
        )
        simulation.start_job(job.job_id)
        simulation.wait_for_job(job.job_id)
        state = simulation.state_manager.get(job.job_id)
        result = simulation.results_database.get(job.job_id)
    finally:
        simulation.shutdown()

    assert state.status == "completed"
    assert result.output["steps_completed"] == 90
    assert result.duration_seconds >= 0.0