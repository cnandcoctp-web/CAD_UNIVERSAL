"""Point primitives for the EvilTech CAD geometry kernel."""

from __future__ import annotations

import math
from dataclasses import dataclass

from GEOMETRY.vector import Vector3D
from MATH_ENGINE.transforms import Transform as MathTransform


@dataclass(slots=True)
class Point3D:
    """A point in three-dimensional space."""

    x: float
    y: float
    z: float

    def __post_init__(self) -> None:
        """Validate that the point coordinates are finite and numeric."""
        for name, value in (("x", self.x), ("y", self.y), ("z", self.z)):
            if not isinstance(value, (int, float)):
                raise TypeError(f"Point coordinate '{name}' must be numeric")
            if not math.isfinite(float(value)):
                raise ValueError(f"Point coordinate '{name}' must be finite")

    def translate(self, vector: Vector3D) -> "Point3D":
        """Translate the point by a vector."""
        if not isinstance(vector, Vector3D):
            raise TypeError("vector must be a Vector3D")
        return Point3D(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def distance_to(self, other: "Point3D") -> float:
        """Return the Euclidean distance to another point."""
        if not isinstance(other, Point3D):
            raise TypeError("other must be a Point3D")
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def transform(self, transform: MathTransform | object) -> "Point3D":
        """Apply an affine transformation to the point."""
        if isinstance(transform, object) and not hasattr(transform, "transform"):
            if not isinstance(transform, MathTransform):
                raise TypeError("transform must be a Transform")
        if hasattr(transform, "transform") and not isinstance(transform, MathTransform):
            transform = transform.transform
        transformed = transform.transform_point(Vector3D(self.x, self.y, self.z).to_math_vector())
        return Point3D(transformed.x, transformed.y, transformed.z)

    def to_dict(self) -> dict[str, float]:
        """Serialize the point to a dictionary."""
        return {"x": self.x, "y": self.y, "z": self.z}
