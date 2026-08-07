"""Mesh primitives for the EvilTech CAD geometry kernel."""

from __future__ import annotations

from dataclasses import dataclass, field

from GEOMETRY.point import Point3D
from GEOMETRY.topology import BoundingBox, MeshTopology
from GEOMETRY.vector import Vector3D


@dataclass(slots=True)
class Mesh:
    """A lightweight polygon mesh container."""

    vertices: list[Point3D]
    faces: list[tuple[int, ...]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.vertices:
            raise ValueError("Mesh requires at least one vertex")
        for vertex in self.vertices:
            if not isinstance(vertex, Point3D):
                raise TypeError("Mesh vertices must be Point3D instances")
        for face in self.faces:
            if len(face) < 3:
                raise ValueError("Mesh faces must contain at least three vertex indices")

    def topology(self) -> MeshTopology:
        """Return the mesh topology view."""
        return MeshTopology(vertices=list(self.vertices))

    def bounding_box(self) -> BoundingBox:
        """Return the mesh axis-aligned bounding box."""
        return BoundingBox(points=list(self.vertices))

    def translate(self, vector: Vector3D) -> "Mesh":
        """Translate the mesh by a vector."""
        return Mesh(vertices=[vertex.translate(vector) for vertex in self.vertices], faces=list(self.faces))

    def face_count(self) -> int:
        """Return the number of mesh faces."""
        return len(self.faces)

    def to_dict(self) -> dict[str, object]:
        """Serialize the mesh to a dictionary."""
        return {
            "vertices": [vertex.to_dict() for vertex in self.vertices],
            "faces": [list(face) for face in self.faces],
        }
