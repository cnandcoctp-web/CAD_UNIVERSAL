"""Arc primitives for the EvilTech CAD geometry kernel."""

from __future__ import annotations

import math
from dataclasses import dataclass

from GEOMETRY.circle import Circle
from GEOMETRY.point import Point3D
from MATH_ENGINE.transforms import Transform as MathTransform


@dataclass(slots=True)
class Arc(Circle):
    """A circular arc defined by a center, radius, and angular bounds."""

    start_angle: float = 0.0
    end_angle: float = 0.0

    def __post_init__(self) -> None:
        """Validate the arc definition."""
        Circle.__post_init__(self)
        if not isinstance(self.start_angle, (int, float)) or not isinstance(self.end_angle, (int, float)):
            raise TypeError("angles must be numeric")
        if self.end_angle < self.start_angle:
            raise ValueError("end_angle must be greater than or equal to start_angle")

    def length(self) -> float:
        """Return the arc length."""
        return self.radius * abs(self.end_angle - self.start_angle)

    def transform(self, transform: MathTransform | object) -> "Arc":
        """Apply an affine transformation to the arc."""
        if hasattr(transform, "transform") and not isinstance(transform, MathTransform):
            transform = transform.transform
        if not isinstance(transform, MathTransform):
            raise TypeError("transform must be a Transform")
        return Arc(self.center.transform(transform), self.radius, self.start_angle, self.end_angle)

    def to_dict(self) -> dict[str, object]:
        """Serialize the arc to a dictionary."""
        base = super().to_dict()
        base.update({"start_angle": self.start_angle, "end_angle": self.end_angle})
        return base
