"""Material database integration for engineering disciplines."""

from __future__ import annotations

from DATA.materials import build_material_library
from ENGINEERING.engineering_models import DisciplineType


class EngineeringMaterialIntegration:
    """Provide access to the shared materials library."""

    def __init__(self) -> None:
        self._library = build_material_library()

    def list_materials_for_discipline(self, discipline: DisciplineType) -> list[dict[str, object]]:
        """Return all shared materials as discipline-usable records."""
        return [
            {
                "key": key,
                "name": material.name,
                "density_kg_m3": material.density_kg_m3,
                "yield_strength_mpa": material.yield_strength_mpa,
                "manufacturability": material.manufacturability,
                "discipline": discipline.value,
            }
            for key, material in self._library.entries.items()
        ]