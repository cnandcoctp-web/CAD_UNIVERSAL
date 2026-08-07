"""Material definitions for rendering."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Material:
    """A serializable material definition for a renderable object."""

    name: str
    color: tuple[float, float, float]
    opacity: float = 1.0

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must be non-empty")
        if len(self.color) != 3:
            raise ValueError("color must contain exactly three components")
        if any(component < 0.0 or component > 1.0 for component in self.color):
            raise ValueError("color components must be within [0, 1]")
        if self.opacity < 0.0 or self.opacity > 1.0:
            raise ValueError("opacity must be within [0, 1]")


class MaterialLibrary:
    """Register and resolve material definitions."""

    def __init__(self) -> None:
        self._materials: dict[str, Material] = {}

    def register(self, material: Material) -> None:
        """Register a material definition."""
        if not isinstance(material, Material):
            raise TypeError("material must be a Material")
        self._materials[material.name] = material

    def get(self, name: str) -> Material:
        """Return a material by name."""
        if name not in self._materials:
            raise KeyError(f"Material '{name}' was not found")
        return self._materials[name]
