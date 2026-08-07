"""Polygon primitives for the EvilTech CAD geometry kernel."""

from __future__ import annotations

from dataclasses import dataclass

from GEOMETRY.point import Point3D
from MATH_ENGINE.transforms import Transform as MathTransform


@dataclass(slots=True)
class Polygon:
    """A polygon defined by a closed sequence of vertices."""

    points: list[Point3D]

    def __post_init__(self) -> None:
        """Validate the polygon vertices."""
        if len(self.points) < 3:
            raise ValueError("Polygon requires at least three points")
        for point in self.points:
            if not isinstance(point, Point3D):
                raise TypeError("All polygon points must be Point3D instances")

    def area(self) -> float:
        """Return the signed area of the polygon in the XY plane."""
        total = 0.0
        for index in range(len(self.points)):
            current = self.points[index]
            next_point = self.points[(index + 1) % len(self.points)]
            total += current.x * next_point.y - next_point.x * current.y
        return abs(total) / 2.0

    def perimeter(self) -> float:
        """Return the perimeter of the polygon."""
        total = 0.0
        for index in range(len(self.points)):
            current = self.points[index]
            next_point = self.points[(index + 1) % len(self.points)]
            total += current.distance_to(next_point)
        return total

    def transform(self, transform: MathTransform | object) -> "Polygon":
        """Apply an affine transformation to the polygon."""
        if hasattr(transform, "transform") and not isinstance(transform, MathTransform):
            transform = transform.transform
        if not isinstance(transform, MathTransform):
            raise TypeError("transform must be a Transform")
        return Polygon([point.transform(transform) for point in self.points])

    def to_dict(self) -> dict[str, object]:
        """Serialize the polygon to a dictionary."""
        return {"points": [point.to_dict() for point in self.points]}
