"""Regression and integration tests for the EvilTech CAD simulation framework."""

from __future__ import annotations

from pathlib import Path

from SIMULATION.simulation_controller import SimulationController
from SIMULATION.simulation_jobs import SimulationJobConfig, SimulationType
from SIMULATION.simulation_manager import SimulationManager


def build_manager(tmp_path: Path) -> SimulationManager:
    return SimulationManager(storage_root=tmp_path / "simulation_runtime", max_workers=3)


def test_simulation_manager_launches_and_executes_sample_job(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    config = SimulationJobConfig(
        name="Static Stress Sample",
        simulation_type=SimulationType.STATIC_STRESS,
        total_steps=6,
        parameters={"mesh_density": "coarse", "discipline": "mechanical"},
    )

    job = manager.create_job(config)
    manager.start_job(job.job_id)
    manager.wait_for_job(job.job_id)
    result = manager.results_database.get(job.job_id)

    assert result.status == "completed"
    assert result.output["simulation_type"] == "static_stress"
    assert result.output["steps_completed"] == 6


def test_controller_supports_pause_resume_and_cancel(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    controller = SimulationController(manager)
    slow_job = controller.create_job(
        name="Thermal Sweep",
        simulation_type=SimulationType.THERMAL_ANALYSIS,
        total_steps=40,
        parameters={"step_delay": 0.003},
    )

    controller.start_job(slow_job.job_id)
    controller.wait_for_progress(slow_job.job_id, minimum_progress=0.1)
    controller.pause_job(slow_job.job_id)
    paused_state = manager.state_manager.get(slow_job.job_id)
    controller.resume_job(slow_job.job_id)
    controller.wait_for_progress(slow_job.job_id, minimum_progress=0.2)

    cancel_job = controller.create_job(
        name="Cancel Motion",
        simulation_type=SimulationType.MOTION_SIMULATION,
        total_steps=50,
        parameters={"step_delay": 0.003},
    )
    controller.start_job(cancel_job.job_id)
    controller.wait_for_progress(cancel_job.job_id, minimum_progress=0.05)
    controller.cancel_job(cancel_job.job_id)
    controller.wait_for_job(cancel_job.job_id)
    cancelled_state = manager.state_manager.get(cancel_job.job_id)

    assert paused_state.status == "paused"
    assert cancelled_state.status == "cancelled"


def test_scheduler_queue_and_multiple_simultaneous_jobs_are_stable(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    created_ids: list[str] = []
    for index, simulation_type in enumerate(
        [
            SimulationType.STRUCTURAL_ANALYSIS,
            SimulationType.HEAT_TRANSFER,
            SimulationType.FLUID_DYNAMICS_FRAMEWORK,
            SimulationType.KINEMATICS,
            SimulationType.ORBITAL_MECHANICS_FRAMEWORK,
        ]
    ):
        job = manager.create_job(
            SimulationJobConfig(
                name=f"Job-{index}",
                simulation_type=simulation_type,
                total_steps=10,
                parameters={"step_delay": 0.002},
            )
        )
        created_ids.append(job.job_id)
        manager.start_job(job.job_id)

    for job_id in created_ids:
        manager.wait_for_job(job_id)

    statuses = {manager.state_manager.get(job_id).status for job_id in created_ids}

    assert statuses == {"completed"}
    assert manager.scheduler.active_count() == 0
    assert manager.queue.is_empty() is True


def test_checkpoint_persistence_and_recovery_resume_jobs(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    job = manager.create_job(
        SimulationJobConfig(
            name="Recoverable Dynamic Stress",
            simulation_type=SimulationType.DYNAMIC_STRESS,
            total_steps=30,
            parameters={"step_delay": 0.003, "checkpoint_interval": 4},
        )
    )

    manager.start_job(job.job_id)
    manager.wait_for_progress(job.job_id, minimum_progress=0.2)
    manager.pause_job(job.job_id)
    checkpoint = manager.recovery_manager.save_checkpoint(job.job_id)

    restored = SimulationManager(storage_root=tmp_path / "simulation_runtime", max_workers=2)
    restored.recovery_manager.restore_job(checkpoint)
    restored.resume_job(job.job_id)
    restored.wait_for_job(job.job_id)

    state = restored.state_manager.get(job.job_id)
    result = restored.results_database.get(job.job_id)

    assert checkpoint.exists()
    assert state.status == "completed"
    assert result.output["steps_completed"] == 30


def test_history_cache_and_results_database_track_runs(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    job = manager.create_job(
        SimulationJobConfig(
            name="Cache Test",
            simulation_type=SimulationType.MATERIAL_BEHAVIOUR,
            total_steps=8,
            parameters={"material": "aluminum-6061"},
        )
    )
    manager.start_job(job.job_id)
    manager.wait_for_job(job.job_id)

    state = manager.state_manager.get(job.job_id)
    history = manager.history.entries(job.job_id)
    cached = manager.cache.get(job.cache_key)
    stored = manager.results_database.get(job.job_id)

    assert state.status == "completed"
    assert any(entry["status"] == "running" for entry in history)
    assert cached is not None
    assert stored.job_id == job.job_id


def test_resource_monitor_logger_and_threading_manager_expose_metrics(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    job = manager.create_job(
        SimulationJobConfig(
            name="Metrics Test",
            simulation_type=SimulationType.ELECTROMAGNETIC_FRAMEWORK,
            total_steps=12,
            parameters={"step_delay": 0.002},
        )
    )
    manager.start_job(job.job_id)
    manager.wait_for_job(job.job_id)

    metrics = manager.resource_monitor.snapshot()
    thread_report = manager.threading_manager.report()
    log_entries = manager.logger.entries(job.job_id)

    assert metrics["completed_jobs"] >= 1
    assert thread_report["max_workers"] == 3
    assert any(entry["event"] == "completed" for entry in log_entries)


def test_stress_long_running_jobs_and_performance(tmp_path: Path) -> None:
    manager = build_manager(tmp_path)
    job_ids: list[str] = []
    for index in range(12):
        job = manager.create_job(
            SimulationJobConfig(
                name=f"Long-{index}",
                simulation_type=SimulationType.FATIGUE_ANALYSIS,
                total_steps=15,
                parameters={"step_delay": 0.001},
            )
        )
        job_ids.append(job.job_id)
        manager.start_job(job.job_id)

    for job_id in job_ids:
        manager.wait_for_job(job_id)

    scalability = manager.scalability_report()

    assert scalability["completed_jobs"] == 12
    assert scalability["failed_jobs"] == 0
    assert scalability["average_duration_seconds"] >= 0.0