"""Progress monitoring helpers for simulation jobs."""

from __future__ import annotations

from time import monotonic

from SIMULATION.simulation_state_manager import SimulationStateManager


class ProgressMonitor:
    """Observe progress of running simulation jobs."""

    def __init__(self, state_manager: SimulationStateManager) -> None:
        self.state_manager = state_manager

    def wait_for_progress(self, job_id: str, minimum_progress: float, timeout_seconds: float = 5.0) -> None:
        """Wait until a job reaches a minimum progress threshold."""
        deadline = monotonic() + timeout_seconds
        while monotonic() < deadline:
            if self.state_manager.get(job_id).progress >= minimum_progress:
                return
        raise TimeoutError(f"Timed out waiting for progress on job '{job_id}'")