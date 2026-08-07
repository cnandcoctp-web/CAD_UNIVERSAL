"""Command console primitives for the EvilTech CAD UI framework."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CommandConsole:
    """A lightweight command console for logging commands and responses."""

    history: list[str] = field(default_factory=list)

    def execute(self, command: str) -> str:
        """Record and echo a command string.

        Args:
            command: The command text to execute.

        Returns:
            A simple execution summary.
        """
        if not isinstance(command, str) or not command.strip():
            raise ValueError("command must be a non-empty string")
        self.history.append(command)
        return f"executed:{command.strip()}"

    def latest(self) -> str | None:
        """Return the most recently executed command, if any."""
        return self.history[-1] if self.history else None
