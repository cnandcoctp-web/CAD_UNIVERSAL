"""Solid primitives for the EvilTech CAD geometry kernel."""

from __future__ import annotations

from dataclasses import dataclass, field

from GEOMETRY.mesh import Mesh
from GEOMETRY.point import Point3D
from GEOMETRY.topology import BoundingBox, SolidTopology
from GEOMETRY.vector import Vector3D


@dataclass(slots=True)
class Solid:
    """A lightweight solid body represented by vertices and optional mesh shells."""

    name: str
    vertices: list[Point3D]
    shells: list[Mesh] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Solid name must be non-empty")
        if len(self.vertices) < 4:
            raise ValueError("Solid requires at least four vertices")

    def topology(self) -> SolidTopology:
        """Return the solid topology view."""
        return SolidTopology(vertices=list(self.vertices))

    def bounding_box(self) -> BoundingBox:
        """Return the solid axis-aligned bounding box."""
        return BoundingBox(points=list(self.vertices))

    def volume(self) -> float:
        """Approximate the solid volume using the bounding box."""
        return self.bounding_box().volume()

    def translate(self, vector: Vector3D) -> "Solid":
        """Translate the solid by a vector."""
        return Solid(
            name=self.name,
            vertices=[vertex.translate(vector) for vertex in self.vertices],
            shells=[shell.translate(vector) for shell in self.shells],
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize the solid to a dictionary."""
        return {
            "name": self.name,
            "vertices": [vertex.to_dict() for vertex in self.vertices],
            "shells": [shell.to_dict() for shell in self.shells],
        }
