"""Scale tools for EvilTech CAD."""

from __future__ import annotations

from GEOMETRY.mesh import Mesh
from GEOMETRY.point import Point3D
from GEOMETRY.solid import Solid


def scale_point(point: Point3D, factor: float) -> Point3D:
    """Uniformly scale a point from the origin."""
    return Point3D(point.x * factor, point.y * factor, point.z * factor)


def scale_mesh(mesh: Mesh, factor: float) -> Mesh:
    """Uniformly scale all mesh vertices."""
    return Mesh(vertices=[scale_point(vertex, factor) for vertex in mesh.vertices], faces=list(mesh.faces))


def scale_solid(solid: Solid, factor: float) -> Solid:
    """Uniformly scale all solid vertices and shells."""
    return Solid(
        name=solid.name,
        vertices=[scale_point(vertex, factor) for vertex in solid.vertices],
        shells=[scale_mesh(shell, factor) for shell in solid.shells],
    )
