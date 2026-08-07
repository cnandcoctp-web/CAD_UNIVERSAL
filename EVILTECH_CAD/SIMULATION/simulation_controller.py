"""User-facing control surface for the simulation framework."""

from __future__ import annotations

from SIMULATION.simulation_jobs import SimulationJob, SimulationJobConfig, SimulationType
from SIMULATION.simulation_manager import SimulationManager


class SimulationController:
    """Facade over the simulation manager."""

    def __init__(self, manager: SimulationManager) -> None:
        self.manager = manager

    def create_job(self, name: str, simulation_type: SimulationType, total_steps: int, parameters: dict[str, object] | None = None) -> SimulationJob:
        """Create a simulation job through the manager."""
        return self.manager.create_job(SimulationJobConfig(name=name, simulation_type=simulation_type, total_steps=total_steps, parameters=dict(parameters or {})))

    def start_job(self, job_id: str) -> None:
        """Start a job."""
        self.manager.start_job(job_id)

    def pause_job(self, job_id: str) -> None:
        """Pause a running job."""
        self.manager.pause_job(job_id)

    def resume_job(self, job_id: str) -> None:
        """Resume a paused job."""
        self.manager.resume_job(job_id)

    def cancel_job(self, job_id: str) -> None:
        """Cancel an active or queued job."""
        self.manager.cancel_job(job_id)

    def wait_for_progress(self, job_id: str, minimum_progress: float) -> None:
        """Wait for a minimum progress threshold."""
        self.manager.wait_for_progress(job_id, minimum_progress)

    def wait_for_job(self, job_id: str) -> None:
        """Wait for job completion."""
        self.manager.wait_for_job(job_id)