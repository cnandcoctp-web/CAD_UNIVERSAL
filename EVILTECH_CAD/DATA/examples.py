"""Example project definitions for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from DATA.libraries import Catalog


@dataclass(slots=True)
class ExampleProject:
    """A reproducible example project descriptor."""

    name: str
    template: str
    description: str
    metadata: dict[str, Any] = field(default_factory=dict)


def build_example_library() -> Catalog[ExampleProject]:
    """Create the default example-project catalog."""
    catalog = Catalog[ExampleProject](name="examples")
    catalog.register("simple-bracket", ExampleProject("Simple Bracket", "mechanical-part", "Two-hole mounting bracket", {"features": ["extrude", "hole", "fillet"]}))
    catalog.register("bearing-block", ExampleProject("Bearing Block", "assembly", "Pedestal with insert bearing", {"parts": 3}))
    catalog.register("gear-train", ExampleProject("Gear Train", "assembly", "Two-stage spur gear reduction", {"parts": 5}))
    return catalog
