"""Surface primitives for the EvilTech CAD geometry kernel."""

from __future__ import annotations

from dataclasses import dataclass

from GEOMETRY.point import Point3D
from MATH_ENGINE.transforms import Transform as MathTransform


@dataclass(slots=True)
class Surface:
    """A planar surface defined by a sequence of boundary points."""

    points: list[Point3D]

    def __post_init__(self) -> None:
        """Validate the surface boundary points."""
        if len(self.points) < 3:
            raise ValueError("Surface requires at least three points")
        for point in self.points:
            if not isinstance(point, Point3D):
                raise TypeError("All surface points must be Point3D instances")

    def area(self) -> float:
        """Return the planar area of the surface."""
        if len(self.points) < 4:
            return 0.0
        return abs((self.points[0].x * self.points[1].y + self.points[1].x * self.points[2].y + self.points[2].x * self.points[3].y + self.points[3].x * self.points[0].y) - (self.points[0].y * self.points[1].x + self.points[1].y * self.points[2].x + self.points[2].y * self.points[3].x + self.points[3].y * self.points[0].x)) / 2.0

    def transform(self, transform: MathTransform | object) -> "Surface":
        """Apply an affine transformation to the surface."""
        if hasattr(transform, "transform") and not isinstance(transform, MathTransform):
            transform = transform.transform
        if not isinstance(transform, MathTransform):
            raise TypeError("transform must be a Transform")
        return Surface([point.transform(transform) for point in self.points])

    def to_dict(self) -> dict[str, object]:
        """Serialize the surface to a dictionary."""
        return {"points": [point.to_dict() for point in self.points]}
