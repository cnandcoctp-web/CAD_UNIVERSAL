"""Sample engineering project generation."""

from __future__ import annotations

from IO.file_manager import ProjectSnapshot

from ENGINEERING.engineering_models import DisciplineType
from ENGINEERING.engineering_registry import EngineeringRegistry


class SampleEngineeringProjectGenerator:
    """Build deterministic sample project payloads per discipline."""

    def __init__(self, registry: EngineeringRegistry) -> None:
        self.registry = registry

    def generate(self, snapshot: ProjectSnapshot, discipline: DisciplineType) -> dict[str, object]:
        """Generate a sample engineering project summary."""
        spec = self.registry.get(discipline)
        return {
            "project_id": snapshot.metadata.project_id,
            "project_name": snapshot.metadata.name,
            "discipline": discipline.value,
            "default_calculation": spec.default_calculation_name,
            "standards": list(spec.standards),
            "design_rules": list(spec.design_rules),
        }