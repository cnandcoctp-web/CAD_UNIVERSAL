"""Future expansion interfaces for engineering disciplines."""

from __future__ import annotations

from ENGINEERING.engineering_models import DisciplineType
from ENGINEERING.engineering_registry import EngineeringRegistry


class FutureExpansionInterfaces:
    """Expose future expansion hooks by discipline."""

    def __init__(self, registry: EngineeringRegistry) -> None:
        self.registry = registry

    def list_for_discipline(self, discipline: DisciplineType) -> list[str]:
        """Return future interface hooks for a discipline."""
        return list(self.registry.get(discipline).future_interfaces)