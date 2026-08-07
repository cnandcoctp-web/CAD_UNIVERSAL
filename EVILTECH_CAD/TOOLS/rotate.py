"""Rotation tools for EvilTech CAD."""

from __future__ import annotations

from GEOMETRY.point import Point3D
from MATH_ENGINE.transforms import Transform


def rotate_point_z(point: Point3D, angle_degrees: float) -> Point3D:
    """Rotate a point around the Z axis."""
    transform = Transform.rotation_z(angle_degrees)
    return point.transform(transform)
