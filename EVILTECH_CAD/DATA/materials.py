"""Material data library for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass

from DATA.libraries import Catalog


@dataclass(slots=True)
class MaterialSpecification:
    """A lightweight material definition."""

    name: str
    density_kg_m3: float
    yield_strength_mpa: float
    manufacturability: str


def build_material_library() -> Catalog[MaterialSpecification]:
    """Create the default material catalog."""
    catalog = Catalog[MaterialSpecification](name="materials")
    catalog.register("aluminum-6061", MaterialSpecification("Aluminum 6061", 2700.0, 276.0, "high"))
    catalog.register("steel-1018", MaterialSpecification("Steel 1018", 7870.0, 370.0, "medium"))
    catalog.register("abs", MaterialSpecification("ABS", 1040.0, 40.0, "high"))
    catalog.register("titanium-ti6al4v", MaterialSpecification("Titanium Ti-6Al-4V", 4430.0, 880.0, "low"))
    return catalog
