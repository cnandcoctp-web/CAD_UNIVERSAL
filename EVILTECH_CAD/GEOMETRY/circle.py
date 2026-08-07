"""Circle primitives for the EvilTech CAD geometry kernel."""

from __future__ import annotations

import math
from dataclasses import dataclass

from GEOMETRY.point import Point3D
from MATH_ENGINE.transforms import Transform as MathTransform


@dataclass(slots=True)
class Circle:
    """A planar circle represented by a center and radius."""

    center: Point3D
    radius: float

    def __post_init__(self) -> None:
        """Validate the circle definition."""
        if not isinstance(self.center, Point3D):
            raise TypeError("center must be a Point3D")
        if not isinstance(self.radius, (int, float)):
            raise TypeError("radius must be numeric")
        if self.radius <= 0.0:
            raise ValueError("radius must be positive")

    def area(self) -> float:
        """Return the area enclosed by the circle."""
        return math.pi * self.radius * self.radius

    def circumference(self) -> float:
        """Return the circumference of the circle."""
        return 2.0 * math.pi * self.radius

    def transform(self, transform: MathTransform | object) -> "Circle":
        """Apply an affine transformation to the circle."""
        if hasattr(transform, "transform") and not isinstance(transform, MathTransform):
            transform = transform.transform
        if not isinstance(transform, MathTransform):
            raise TypeError("transform must be a Transform")
        return Circle(self.center.transform(transform), self.radius)

    def to_dict(self) -> dict[str, object]:
        """Serialize the circle to a dictionary."""
        return {"center": self.center.to_dict(), "radius": self.radius}
