"""Project templates for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from DATA.libraries import Catalog


@dataclass(slots=True)
class ProjectTemplate:
    """A reusable project template payload."""

    name: str
    description: str
    defaults: dict[str, Any] = field(default_factory=dict)


def build_template_library() -> Catalog[ProjectTemplate]:
    """Create the default project-template catalog."""
    catalog = Catalog[ProjectTemplate](name="templates")
    catalog.register("mechanical-part", ProjectTemplate("Mechanical Part", "Single component part design", {"units": "mm", "material": "aluminum-6061"}))
    catalog.register("assembly", ProjectTemplate("Assembly", "Multi-component assembly design", {"units": "mm", "bom": True}))
    catalog.register("3d-print", ProjectTemplate("3D Print", "Consumer additive manufacturing workflow", {"units": "mm", "material": "abs"}))
    return catalog
