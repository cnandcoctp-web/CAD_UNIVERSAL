"""State manager for simulation jobs."""

from __future__ import annotations

from threading import Lock

from SIMULATION.simulation_jobs import SimulationState


class SimulationStateManager:
    """Store and update simulation job states."""

    def __init__(self) -> None:
        self._states: dict[str, SimulationState] = {}
        self._lock = Lock()

    def register(self, state: SimulationState) -> None:
        """Register a new simulation state."""
        with self._lock:
            self._states[state.job_id] = state

    def get(self, job_id: str) -> SimulationState:
        """Return a simulation state by job identifier."""
        with self._lock:
            return SimulationState.from_dict(self._states[job_id].to_dict())

    def peek(self, job_id: str) -> SimulationState:
        """Return the internal mutable simulation state."""
        with self._lock:
            return self._states[job_id]

    def update(self, job_id: str, **updates: object) -> SimulationState:
        """Update a simulation state in place."""
        with self._lock:
            state = self._states[job_id]
            for key, value in updates.items():
                setattr(state, key, value)
            return state

    def all_states(self) -> list[SimulationState]:
        """Return all registered states."""
        with self._lock:
            return [SimulationState.from_dict(state.to_dict()) for state in self._states.values()]