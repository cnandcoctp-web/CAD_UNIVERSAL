"""Move tools for EvilTech CAD."""

from __future__ import annotations

from GEOMETRY.mesh import Mesh
from GEOMETRY.point import Point3D
from GEOMETRY.solid import Solid
from GEOMETRY.vector import Vector3D


def move_point(point: Point3D, vector: Vector3D) -> Point3D:
    """Translate a point by a vector."""
    return point.translate(vector)


def move_mesh(mesh: Mesh, vector: Vector3D) -> Mesh:
    """Translate a mesh by a vector."""
    return mesh.translate(vector)


def move_solid(solid: Solid, vector: Vector3D) -> Solid:
    """Translate a solid by a vector."""
    return solid.translate(vector)
