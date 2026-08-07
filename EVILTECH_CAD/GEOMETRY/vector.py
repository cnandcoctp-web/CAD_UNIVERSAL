"""Vector primitives for the EvilTech CAD geometry kernel."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterator

from MATH_ENGINE.algebra import Vector3 as MathVector3


@dataclass(slots=True)
class Vector3D:
    """A three-dimensional vector used for direction, displacement, and geometry queries."""

    x: float
    y: float
    z: float

    def __post_init__(self) -> None:
        """Validate that the vector components are finite and numeric."""
        for name, value in (("x", self.x), ("y", self.y), ("z", self.z)):
            if not isinstance(value, (int, float)):
                raise TypeError(f"Vector component '{name}' must be numeric")
            if not math.isfinite(float(value)):
                raise ValueError(f"Vector component '{name}' must be finite")

    def __iter__(self) -> Iterator[float]:
        """Yield the vector components in order."""
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, other: "Vector3D") -> "Vector3D":
        """Add two vectors component-wise."""
        if not isinstance(other, Vector3D):
            raise TypeError("other must be a Vector3D")
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3D") -> "Vector3D":
        """Subtract another vector from this one."""
        if not isinstance(other, Vector3D):
            raise TypeError("other must be a Vector3D")
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Vector3D":
        """Scale the vector by a scalar."""
        if not isinstance(scalar, (int, float)):
            raise TypeError("scalar must be numeric")
        return Vector3D(self.x * float(scalar), self.y * float(scalar), self.z * float(scalar))

    def __rmul__(self, scalar: float) -> "Vector3D":
        """Support scalar multiplication on the left."""
        return self * scalar

    def magnitude(self) -> float:
        """Return the Euclidean length of the vector."""
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalized(self) -> "Vector3D":
        """Return a unit vector in the same direction."""
        length = self.magnitude()
        if length == 0.0:
            raise ValueError("Cannot normalize a zero-length vector")
        return self / length

    def __truediv__(self, scalar: float) -> "Vector3D":
        """Divide the vector by a scalar."""
        if not isinstance(scalar, (int, float)):
            raise TypeError("scalar must be numeric")
        if float(scalar) == 0.0:
            raise ZeroDivisionError("Cannot divide a vector by zero")
        return Vector3D(self.x / float(scalar), self.y / float(scalar), self.z / float(scalar))

    def dot(self, other: "Vector3D") -> float:
        """Compute the dot product with another vector."""
        if not isinstance(other, Vector3D):
            raise TypeError("other must be a Vector3D")
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vector3D") -> "Vector3D":
        """Compute the cross product with another vector."""
        if not isinstance(other, Vector3D):
            raise TypeError("other must be a Vector3D")
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def to_math_vector(self) -> MathVector3:
        """Return the equivalent math-engine vector."""
        return MathVector3(self.x, self.y, self.z)

    @classmethod
    def from_math_vector(cls, vector: MathVector3) -> "Vector3D":
        """Create a geometry vector from a math-engine vector."""
        if not isinstance(vector, MathVector3):
            raise TypeError("vector must be a MathVector3")
        return cls(vector.x, vector.y, vector.z)

    def to_dict(self) -> dict[str, float]:
        """Serialize the vector to a dictionary."""
        return {"x": self.x, "y": self.y, "z": self.z}
