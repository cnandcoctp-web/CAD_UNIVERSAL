"""Design-rules access for engineering disciplines."""

from __future__ import annotations

from ENGINEERING.engineering_models import DisciplineType
from ENGINEERING.engineering_registry import EngineeringRegistry


class EngineeringDesignRules:
    """Expose discipline-specific design rules."""

    def __init__(self, registry: EngineeringRegistry) -> None:
        self.registry = registry

    def list_for_discipline(self, discipline: DisciplineType) -> list[str]:
        """Return design rules for a discipline."""
        return list(self.registry.get(discipline).design_rules)