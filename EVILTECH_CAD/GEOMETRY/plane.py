"""Plane geometry primitives for the EvilTech CAD geometry kernel."""

from __future__ import annotations

import math
from dataclasses import dataclass

from GEOMETRY.point import Point3D
from GEOMETRY.vector import Vector3D
from MATH_ENGINE.transforms import Transform as MathTransform


@dataclass(slots=True)
class Plane:
    """An infinite plane defined by an origin point and two basis vectors."""

    origin: Point3D
    basis_x: Vector3D
    basis_y: Vector3D

    def __post_init__(self) -> None:
        """Validate that the plane definition is well formed."""
        if not isinstance(self.origin, Point3D):
            raise TypeError("origin must be a Point3D")
        for name, value in (("basis_x", self.basis_x), ("basis_y", self.basis_y)):
            if not isinstance(value, Vector3D):
                raise TypeError(f"{name} must be a Vector3D")

    def contains_point(self, point: Point3D) -> bool:
        """Determine whether a point lies on the plane."""
        if not isinstance(point, Point3D):
            raise TypeError("point must be a Point3D")
        offset = Vector3D(point.x - self.origin.x, point.y - self.origin.y, point.z - self.origin.z)
        return abs(offset.dot(self.basis_x.cross(self.basis_y))) < 1e-9

    def transform(self, transform: MathTransform | object) -> "Plane":
        """Apply an affine transformation to the plane."""
        if hasattr(transform, "transform") and not isinstance(transform, MathTransform):
            transform = transform.transform
        if not isinstance(transform, MathTransform):
            raise TypeError("transform must be a Transform")
        return Plane(self.origin.transform(transform), self.basis_x, self.basis_y)

    def to_dict(self) -> dict[str, object]:
        """Serialize the plane to a dictionary."""
        return {"origin": self.origin.to_dict(), "basis_x": self.basis_x.to_dict(), "basis_y": self.basis_y.to_dict()}
