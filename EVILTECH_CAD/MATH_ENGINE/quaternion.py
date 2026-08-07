"""Quaternion mathematics for rotations and orientation handling."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterator

from MATH_ENGINE.algebra import Vector3


@dataclass(slots=True)
class Quaternion:
    """A compact representation of orientation and rotation in 3D space."""

    w: float
    x: float
    y: float
    z: float

    def __post_init__(self) -> None:
        """Validate quaternion components."""
        for name, value in (("w", self.w), ("x", self.x), ("y", self.y), ("z", self.z)):
            if not isinstance(value, (int, float)):
                raise TypeError(f"Quaternion component '{name}' must be numeric")
            if not math.isfinite(float(value)):
                raise ValueError(f"Quaternion component '{name}' must be finite")

    def __iter__(self) -> Iterator[float]:
        """Yield quaternion components."""
        yield self.w
        yield self.x
        yield self.y
        yield self.z

    def norm(self) -> float:
        """Return the quaternion norm."""
        return math.sqrt(self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z)

    def normalized(self) -> "Quaternion":
        """Return a unit quaternion preserving the direction."""
        magnitude = self.norm()
        if magnitude == 0.0:
            raise ValueError("Cannot normalize a zero quaternion")
        return Quaternion(self.w / magnitude, self.x / magnitude, self.y / magnitude, self.z / magnitude)

    def conjugate(self) -> "Quaternion":
        """Return the quaternion conjugate."""
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inverse(self) -> "Quaternion":
        """Return the multiplicative inverse of the quaternion."""
        magnitude_squared = self.norm() ** 2
        if magnitude_squared == 0.0:
            raise ValueError("Cannot invert a zero quaternion")
        conjugate = self.conjugate()
        return Quaternion(conjugate.w / magnitude_squared, conjugate.x / magnitude_squared, conjugate.y / magnitude_squared, conjugate.z / magnitude_squared)

    def __mul__(self, other: "Quaternion") -> "Quaternion":
        """Multiply two quaternions."""
        if not isinstance(other, Quaternion):
            raise TypeError("Expected a Quaternion instance")
        return Quaternion(
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
        )

    def rotate_vector(self, vector: Vector3) -> Vector3:
        """Rotate a vector by this quaternion."""
        if not isinstance(vector, Vector3):
            raise TypeError("Expected a Vector3 instance")
        quaternion = self.normalized()
        q_vector = Quaternion(0.0, vector.x, vector.y, vector.z)
        result = quaternion * q_vector * quaternion.conjugate()
        return Vector3(result.x, result.y, result.z)

    @classmethod
    def from_axis_angle(cls, axis: Vector3, angle: float) -> "Quaternion":
        """Create a quaternion from an axis-angle pair."""
        if not isinstance(axis, Vector3):
            raise TypeError("axis must be a Vector3")
        if not isinstance(angle, (int, float)):
            raise TypeError("angle must be numeric")
        axis_vector = axis.normalized()
        half_angle = float(angle) / 2.0
        scale = math.sin(half_angle)
        return cls(
            math.cos(half_angle),
            axis_vector.x * scale,
            axis_vector.y * scale,
            axis_vector.z * scale,
        )
