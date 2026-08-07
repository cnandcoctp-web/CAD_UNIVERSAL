"""Mirror tools for EvilTech CAD."""

from __future__ import annotations

from GEOMETRY.point import Point3D


def mirror_point_x(point: Point3D) -> Point3D:
    """Mirror a point across the YZ plane."""
    return Point3D(-point.x, point.y, point.z)
