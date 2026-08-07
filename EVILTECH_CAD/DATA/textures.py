"""Texture catalog for EvilTech CAD rendering workflows."""

from __future__ import annotations

from dataclasses import dataclass

from DATA.libraries import Catalog


@dataclass(slots=True)
class TextureDefinition:
    """A texture record with a procedural or file-backed source."""

    name: str
    kind: str
    source: str


def build_texture_library() -> Catalog[TextureDefinition]:
    """Create the default texture catalog."""
    catalog = Catalog[TextureDefinition](name="textures")
    catalog.register("brushed-metal", TextureDefinition("Brushed Metal", "procedural", "noise:anisotropic"))
    catalog.register("matte-plastic", TextureDefinition("Matte Plastic", "procedural", "noise:soft"))
    catalog.register("checkerboard", TextureDefinition("Checkerboard", "procedural", "pattern:checker"))
    return catalog
