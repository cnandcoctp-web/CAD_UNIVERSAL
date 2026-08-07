"""Bearing catalog for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass

from DATA.libraries import Catalog


@dataclass(slots=True)
class BearingSpecification:
    """A rolling bearing definition."""

    name: str
    bore_mm: float
    outer_diameter_mm: float
    width_mm: float


def build_bearing_library() -> Catalog[BearingSpecification]:
    """Create the default bearing catalog."""
    catalog = Catalog[BearingSpecification](name="bearings")
    catalog.register("608-2rs", BearingSpecification("608-2RS", 8.0, 22.0, 7.0))
    catalog.register("6204-2rs", BearingSpecification("6204-2RS", 20.0, 47.0, 14.0))
    catalog.register("6001-zz", BearingSpecification("6001-ZZ", 12.0, 28.0, 8.0))
    return catalog
