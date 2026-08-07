"""Undo and redo support for EvilTech CAD design workflows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(slots=True)
class Command:
    """A reversible command."""

    do: Callable[[], None]
    undo: Callable[[], None]
    description: str = ""


class UndoRedoStack:
    """Store and replay reversible commands."""

    def __init__(self) -> None:
        self._undo_stack: list[Command] = []
        self._redo_stack: list[Command] = []

    def execute(self, command: Command) -> None:
        """Execute and track a command."""
        command.do()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self) -> bool:
        """Undo the latest command."""
        if not self._undo_stack:
            return False
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)
        return True

    def redo(self) -> bool:
        """Redo the latest undone command."""
        if not self._redo_stack:
            return False
        command = self._redo_stack.pop()
        command.do()
        self._undo_stack.append(command)
        return True
