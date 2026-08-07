"""Line geometry primitives for the EvilTech CAD geometry kernel."""

from __future__ import annotations

import math
from dataclasses import dataclass

from GEOMETRY.point import Point3D
from GEOMETRY.vector import Vector3D
from MATH_ENGINE.transforms import Transform as MathTransform


@dataclass(slots=True)
class Line:
    """A straight line segment defined by a start and end point."""

    start: Point3D
    end: Point3D

    def __post_init__(self) -> None:
        """Validate that the line endpoints are valid points."""
        if not isinstance(self.start, Point3D):
            raise TypeError("start must be a Point3D")
        if not isinstance(self.end, Point3D):
            raise TypeError("end must be a Point3D")

    def vector(self) -> Vector3D:
        """Return the direction vector of the line."""
        return Vector3D(self.end.x - self.start.x, self.end.y - self.start.y, self.end.z - self.start.z)

    def length(self) -> float:
        """Return the length of the line segment."""
        return self.start.distance_to(self.end)

    def transform(self, transform: MathTransform | object) -> "Line":
        """Apply an affine transformation to the line."""
        if hasattr(transform, "transform") and not isinstance(transform, MathTransform):
            transform = transform.transform
        if not isinstance(transform, MathTransform):
            raise TypeError("transform must be a Transform")
        return Line(self.start.transform(transform), self.end.transform(transform))

    def to_dict(self) -> dict[str, object]:
        """Serialize the line to a dictionary."""
        return {"start": self.start.to_dict(), "end": self.end.to_dict()}
