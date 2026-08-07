"""Discipline-specific engineering library access."""

from __future__ import annotations

from ENGINEERING.engineering_models import DisciplineType
from ENGINEERING.engineering_registry import EngineeringRegistry


class DisciplineLibraries:
    """Expose per-discipline reference library content."""

    def __init__(self, registry: EngineeringRegistry) -> None:
        self.registry = registry

    def get_library(self, discipline: DisciplineType) -> dict[str, object]:
        """Return the discipline-specific library payload."""
        return dict(self.registry.get(discipline).library)