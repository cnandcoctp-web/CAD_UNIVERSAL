"""Runtime metrics for the simulation framework."""

from __future__ import annotations

from SIMULATION.simulation_state_manager import SimulationStateManager


class ResourceMonitor:
    """Provide lightweight framework resource and status metrics."""

    def __init__(self, state_manager: SimulationStateManager) -> None:
        self.state_manager = state_manager

    def snapshot(self) -> dict[str, int]:
        """Return a snapshot of job counts by state."""
        states = self.state_manager.all_states()
        return {
            "queued_jobs": sum(1 for state in states if state.status == "queued"),
            "active_jobs": sum(1 for state in states if state.status == "running"),
            "paused_jobs": sum(1 for state in states if state.status == "paused"),
            "completed_jobs": sum(1 for state in states if state.status == "completed"),
            "failed_jobs": sum(1 for state in states if state.status == "failed"),
            "cancelled_jobs": sum(1 for state in states if state.status == "cancelled"),
        }