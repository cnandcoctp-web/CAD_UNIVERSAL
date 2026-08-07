"""Fastener catalog for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass

from DATA.libraries import Catalog


@dataclass(slots=True)
class FastenerSpecification:
    """A standard fastener definition."""

    name: str
    diameter_mm: float
    length_mm: float
    standard: str


def build_fastener_library() -> Catalog[FastenerSpecification]:
    """Create the default fastener catalog."""
    catalog = Catalog[FastenerSpecification](name="fasteners")
    catalog.register("iso-4762-m6x20", FastenerSpecification("Socket Head Cap Screw M6x20", 6.0, 20.0, "ISO 4762"))
    catalog.register("din-934-m6", FastenerSpecification("Hex Nut M6", 6.0, 5.0, "DIN 934"))
    catalog.register("iso-7089-m6", FastenerSpecification("Plain Washer M6", 6.4, 1.6, "ISO 7089"))
    return catalog
