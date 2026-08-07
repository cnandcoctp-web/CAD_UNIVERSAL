"""Status and workflow manager primitives for the EvilTech CAD UI framework."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class NotificationCenter:
    """A simple notification collector."""

    messages: list[str] = field(default_factory=list)

    def publish(self, message: str) -> None:
        """Publish a notification message."""
        if not isinstance(message, str) or not message.strip():
            raise ValueError("message must be a non-empty string")
        self.messages.append(message)

    def latest(self) -> str | None:
        """Return the latest notification message."""
        return self.messages[-1] if self.messages else None


class ProgressManager:
    """Track named progress values for UI workflows."""

    def __init__(self) -> None:
        self._values: dict[str, float] = {}

    def update(self, key: str, progress: float) -> None:
        """Update a progress value in the inclusive range [0, 1]."""
        if not isinstance(progress, (int, float)):
            raise TypeError("progress must be numeric")
        if progress < 0.0 or progress > 1.0:
            raise ValueError("progress must be within [0, 1]")
        self._values[key] = float(progress)

    def get(self, key: str) -> float:
        """Return a progress value by key."""
        return self._values[key]


class TaskManager:
    """Track task lifecycle state for UI workflows."""

    def __init__(self) -> None:
        self._tasks: dict[str, str] = {}

    def start_task(self, name: str) -> None:
        """Mark a task as running."""
        self._tasks[name] = "running"

    def complete_task(self, name: str) -> None:
        """Mark a task as completed."""
        if name not in self._tasks:
            raise KeyError(f"Task '{name}' was not found")
        self._tasks[name] = "completed"

    def status_of(self, name: str) -> str:
        """Return the status of a tracked task."""
        return self._tasks[name]


@dataclass(slots=True)
class SimulationStatusPanel:
    """Display simulation status without implementing simulation logic."""

    status: str = "idle"

    def set_status(self, status: str) -> None:
        """Set the simulation status label."""
        if not isinstance(status, str) or not status.strip():
            raise ValueError("status must be a non-empty string")
        self.status = status


@dataclass(slots=True)
class StatusBar:
    """Aggregate status subcomponents for the main window."""

    notifications: NotificationCenter
    progress: ProgressManager
    tasks: TaskManager
    simulation: SimulationStatusPanel
