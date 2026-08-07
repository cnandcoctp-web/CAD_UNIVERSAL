"""Live design-state tracking for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class SelectionState:
    """Track the current selection."""

    selected_ids: list[str] = field(default_factory=list)
    active_tool: str | None = None


@dataclass(slots=True)
class DesignState:
    """Mutable design-session state."""

    project_name: str
    selection: SelectionState = field(default_factory=SelectionState)
    dirty: bool = False
    active_workspace: str = "modeling"


class DesignStateManager:
    """Create and mutate design state records."""

    def create(self, project_name: str) -> DesignState:
        """Create a new design-state instance."""
        return DesignState(project_name=project_name)

    def mark_dirty(self, state: DesignState, dirty: bool = True) -> None:
        """Mark the state as having unsaved changes."""
        state.dirty = dirty

    def select(self, state: DesignState, *identifiers: str) -> None:
        """Replace the current selection."""
        state.selection.selected_ids = [identifier for identifier in identifiers if identifier]
