"""Spline primitives for the EvilTech CAD geometry kernel."""

from __future__ import annotations

from dataclasses import dataclass

from GEOMETRY.point import Point3D
from MATH_ENGINE.transforms import Transform as MathTransform


@dataclass(slots=True)
class Spline:
    """A lightweight spline represented by a sequence of control points."""

    points: list[Point3D]

    def __post_init__(self) -> None:
        """Validate the spline control points."""
        if not self.points:
            raise ValueError("Spline requires at least one control point")
        for point in self.points:
            if not isinstance(point, Point3D):
                raise TypeError("All spline points must be Point3D instances")

    def transform(self, transform: MathTransform | object) -> "Spline":
        """Apply an affine transformation to the spline."""
        if hasattr(transform, "transform") and not isinstance(transform, MathTransform):
            transform = transform.transform
        if not isinstance(transform, MathTransform):
            raise TypeError("transform must be a Transform")
        return Spline([point.transform(transform) for point in self.points])

    def to_dict(self) -> dict[str, object]:
        """Serialize the spline to a dictionary."""
        return {"points": [point.to_dict() for point in self.points]}
