"""Regression and integration tests for the EvilTech CAD engineering modules."""

from __future__ import annotations

from pathlib import Path

import pytest

from AI.engineering_assistant import EngineeringAssistant
from IO.file_manager import ProjectManager
from SIMULATION.simulation_jobs import SimulationType
from SIMULATION.simulation_manager import SimulationManager

from ENGINEERING.engineering_manager import EngineeringManager
from ENGINEERING.engineering_models import DisciplineType


def build_manager(tmp_path: Path) -> EngineeringManager:
    return EngineeringManager(storage_root=tmp_path / "engineering_runtime")


def test_registry_exposes_all_engineering_disciplines(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)

    assert set(manager.registry.discipline_names()) == {
        "mechanical_engineering",
        "civil_engineering",
        "structural_engineering",
        "architecture",
        "electrical_engineering",
        "plumbing",
        "hvac",
        "manufacturing",
        "materials_engineering",
        "robotics",
        "automotive_engineering",
        "aerospace_engineering",
        "thermodynamics",
        "combustion_engineering",
        "fluid_mechanics",
        "astronomy",
        "orbital_mechanics",
        "scientific_calculations",
    }


def test_calculation_and_validation_engines_produce_deterministic_results(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    request = manager.create_calculation_request(
        discipline=DisciplineType.MECHANICAL_ENGINEERING,
        calculation_name="beam_bending_stress",
        inputs={"moment_nm": 1200.0, "section_modulus_mm3": 60000.0},
    )

    result = manager.run_calculation(request)

    assert result.valid is True
    assert result.value == pytest.approx(20.0, rel=1e-5)
    assert result.unit == "MPa"
    assert manager.validation_engine.validate_request(request).is_valid is True


def test_cross_discipline_accuracy_and_standards_access(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    civil = manager.run_calculation(
        manager.create_calculation_request(
            discipline=DisciplineType.CIVIL_ENGINEERING,
            calculation_name="slab_load",
            inputs={"area_m2": 30.0, "pressure_kpa": 6.0},
        )
    )
    electrical = manager.run_calculation(
        manager.create_calculation_request(
            discipline=DisciplineType.ELECTRICAL_ENGINEERING,
            calculation_name="ohms_law_current",
            inputs={"voltage_v": 24.0, "resistance_ohm": 8.0},
        )
    )
    orbital = manager.run_calculation(
        manager.create_calculation_request(
            discipline=DisciplineType.ORBITAL_MECHANICS,
            calculation_name="orbital_velocity",
            inputs={"gravitational_parameter": 398600.4418, "radius_km": 7000.0},
        )
    )
    standards = manager.standards_framework.list_for_discipline(DisciplineType.MANUFACTURING)

    assert civil.value == pytest.approx(180.0)
    assert electrical.value == pytest.approx(3.0)
    assert orbital.value == pytest.approx(7.546053, rel=1e-4)
    assert standards


def test_material_database_integration_analysis_tools_and_optimization(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    materials = manager.material_integration.list_materials_for_discipline(DisciplineType.MATERIALS_ENGINEERING)
    analysis = manager.analysis_tools.evaluate(
        DisciplineType.STRUCTURAL_ENGINEERING,
        {"safety_factor": 1.8, "mass_kg": 24.0, "compliance": 0.92},
    )
    optimization = manager.optimization_utilities.optimize(
        DisciplineType.AUTOMOTIVE_ENGINEERING,
        baseline={"mass_kg": 1200.0, "drag_coefficient": 0.32},
        objective="reduce_mass",
    )

    assert materials
    assert analysis["status"] == "pass"
    assert optimization["objective"] == "reduce_mass"
    assert optimization["recommended_changes"]


def test_reports_and_sample_engineering_projects_are_generated(tmp_path: Path) -> None:
    project_manager = ProjectManager()
    snapshot = project_manager.create_new_project("Engineering Sample", tmp_path / "engineering_sample")
    manager = build_manager(tmp_path)
    sample = manager.sample_project_generator.generate(snapshot, DisciplineType.HVAC)
    request = manager.create_calculation_request(
        discipline=DisciplineType.HVAC,
        calculation_name="air_change_rate",
        inputs={"airflow_m3_s": 2.5, "room_volume_m3": 300.0},
    )
    result = manager.run_calculation(request)
    report = manager.report_generator.generate(snapshot.metadata.project_id, sample, result)

    assert sample["discipline"] == "hvac"
    assert report["project_id"] == snapshot.metadata.project_id
    assert report["calculation"]["value"] == pytest.approx(30.0)


def test_ai_and_simulation_integration_interfaces(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    assistant = EngineeringAssistant()
    simulation_manager = SimulationManager(storage_root=tmp_path / "sim_runtime", max_workers=2)

    ai_payload = manager.ai_integration.build_review_payload(
        assistant=assistant,
        discipline=DisciplineType.MANUFACTURING,
        context_summary="Tolerance stack-up and manufacturability review",
    )
    simulation_request = manager.simulation_integration.build_request(
        discipline=DisciplineType.THERMODYNAMICS,
        simulation_type=SimulationType.THERMAL_ANALYSIS,
        parameters={"boundary_case": "steady_state"},
    )
    job = simulation_manager.create_job(simulation_request.to_job_config(name="Thermal Framework Probe", total_steps=8))
    simulation_manager.start_job(job.job_id)
    simulation_manager.wait_for_job(job.job_id)

    assert ai_payload["discipline"] == "manufacturing"
    assert simulation_request.simulation_type is SimulationType.THERMAL_ANALYSIS
    assert simulation_manager.results_database.get(job.job_id).status == "completed"


def test_stress_performance_and_cross_discipline_integration(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    requests = []
    for discipline in DisciplineType:
        requests.append(
            manager.create_calculation_request(
                discipline=discipline,
                calculation_name=manager.registry.default_calculation_name(discipline),
                inputs=manager.registry.sample_inputs(discipline),
            )
        )

    results = [manager.run_calculation(request) for request in requests]
    summary = manager.validation_summary(results)

    assert len(results) == len(DisciplineType)
    assert summary["valid_results"] == len(DisciplineType)
    assert summary["average_duration_seconds"] >= 0.0
