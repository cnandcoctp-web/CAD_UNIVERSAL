"""Gear catalog for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass

from DATA.libraries import Catalog


@dataclass(slots=True)
class GearSpecification:
    """A standard spur-gear definition."""

    name: str
    module_mm: float
    tooth_count: int
    pressure_angle_deg: float


def build_gear_library() -> Catalog[GearSpecification]:
    """Create the default gear catalog."""
    catalog = Catalog[GearSpecification](name="gears")
    catalog.register("m1-20t", GearSpecification("Module 1 Spur Gear 20T", 1.0, 20, 20.0))
    catalog.register("m2-30t", GearSpecification("Module 2 Spur Gear 30T", 2.0, 30, 20.0))
    catalog.register("m3-15t", GearSpecification("Module 3 Spur Gear 15T", 3.0, 15, 20.0))
    return catalog
