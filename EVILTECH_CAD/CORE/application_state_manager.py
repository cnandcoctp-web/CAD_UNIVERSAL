"""Application state management for the EvilTech CAD foundation layer.

This module provides the canonical runtime state for the application shell.
It is intentionally small, deterministic, and safe for use across the
foundation services that coordinate startup, shutdown, and project lifecycle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from CORE.constants import LifecycleState


@dataclass(slots=True)
class ApplicationStateSnapshot:
    """Immutable snapshot of the application state."""

    state: LifecycleState
    details: Dict[str, Any] = field(default_factory=dict)


class ApplicationStateManager:
    """Track and expose the high-level runtime state for the application."""

    def __init__(self, initial_state: LifecycleState | str = LifecycleState.INITIALIZING) -> None:
        """Initialize the state manager.

        Args:
            initial_state: The initial lifecycle state for the application.
        """
        self._state: LifecycleState = self._coerce_state(initial_state)
        self._details: Dict[str, Any] = {}
        self._listeners: List[Callable[[ApplicationStateSnapshot], None]] = []

    def set_state(self, state: LifecycleState | str, details: Optional[Dict[str, Any]] = None) -> None:
        """Set the current application state.

        Args:
            state: The lifecycle state to assign.
            details: Optional structured details to attach to the new state.
        """
        coerced_state = self._coerce_state(state)
        self._state = coerced_state
        if details:
            self._details = dict(details)
        else:
            self._details = {}
        snapshot = self.snapshot()
        for listener in list(self._listeners):
            listener(snapshot)

    def get_state(self) -> LifecycleState:
        """Return the current application state."""
        return self._state

    def snapshot(self) -> Dict[str, Any]:
        """Return a serializable snapshot of the current application state."""
        return {"state": self._state.value, "details": dict(self._details)}

    def subscribe(self, listener: Callable[[ApplicationStateSnapshot], None]) -> None:
        """Register a listener that receives state updates."""
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unsubscribe(self, listener: Callable[[ApplicationStateSnapshot], None]) -> None:
        """Remove a registered state listener."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    @staticmethod
    def _coerce_state(state: LifecycleState | str) -> LifecycleState:
        """Normalize a state value to a ``LifecycleState`` instance."""
        if isinstance(state, LifecycleState):
            return state
        try:
            return LifecycleState(state)
        except ValueError as exc:
            raise ValueError(f"Unsupported lifecycle state: {state}") from exc
