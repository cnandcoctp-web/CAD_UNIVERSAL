"""Project-scoped memory for the AI Engineering Assistant."""

from __future__ import annotations

from AI.context_builder import AssistantContext


class ProjectMemory:
    """Store assistant contexts and generated artifacts by project."""

    def __init__(self) -> None:
        self._contexts: dict[str, AssistantContext] = {}
        self._reports: dict[str, dict[str, object]] = {}

    def store_context(self, project_id: str, context: AssistantContext) -> None:
        """Store project-level assistant context."""
        self._contexts[project_id] = context

    def get_context(self, project_id: str) -> AssistantContext:
        """Return stored assistant context by project identifier."""
        return self._contexts[project_id]

    def store_report(self, project_id: str, report: dict[str, object]) -> None:
        """Store the latest generated engineering report."""
        self._reports[project_id] = dict(report)

    def get_report(self, project_id: str) -> dict[str, object]:
        """Return the latest generated engineering report."""
        return dict(self._reports[project_id])