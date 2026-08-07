"""Design-standard catalog for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass

from DATA.libraries import Catalog


@dataclass(slots=True)
class DesignStandard:
    """A design standard summary."""

    code: str
    title: str
    domain: str


def build_standard_library() -> Catalog[DesignStandard]:
    """Create the default standards catalog."""
    catalog = Catalog[DesignStandard](name="standards")
    catalog.register("iso-2768", DesignStandard("ISO 2768", "General tolerances", "tolerancing"))
    catalog.register("iso-286", DesignStandard("ISO 286", "ISO system of limits and fits", "fits"))
    catalog.register("asme-y14.5", DesignStandard("ASME Y14.5", "Dimensioning and tolerancing", "documentation"))
    return catalog
