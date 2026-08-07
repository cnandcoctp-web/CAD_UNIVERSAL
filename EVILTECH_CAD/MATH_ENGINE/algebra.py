"""Vector mathematics and coordinate-system utilities for EvilTech CAD.

This module provides the low-level geometric primitives used across the
mathematical engine, including 3D vectors and a simple coordinate frame
abstraction for local/global transforms.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterator, Sequence


@dataclass(slots=True)
class Vector3:
    """A three-dimensional Euclidean vector.

    The class provides the common operations needed for geometry, transforms,
    and numerical routines. All components are stored as floating-point values
    and validated to be finite.
    """

    x: float
    y: float
    z: float

    def __post_init__(self) -> None:
        """Validate that the vector components are finite."""
        self._validate_component(self.x, "x")
        self._validate_component(self.y, "y")
        self._validate_component(self.z, "z")

    @staticmethod
    def _validate_component(value: float, name: str) -> None:
        """Ensure a component is a finite numeric value."""
        if not isinstance(value, (int, float)):
            raise TypeError(f"Vector component '{name}' must be numeric")
        if not math.isfinite(float(value)):
            raise ValueError(f"Vector component '{name}' must be finite")

    def __iter__(self) -> Iterator[float]:
        """Yield the vector components in order."""
        yield self.x
        yield self.y
        yield self.z

    def __len__(self) -> int:
        """Return the dimensionality of the vector."""
        return 3

    def __getitem__(self, index: int) -> float:
        """Access a vector component by index."""
        if index not in (0, 1, 2):
            raise IndexError("Vector3 only supports indices 0, 1, and 2")
        return (self.x, self.y, self.z)[index]

    def __add__(self, other: "Vector3") -> "Vector3":
        """Add another vector component-wise."""
        if not isinstance(other, Vector3):
            return NotImplemented
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3") -> "Vector3":
        """Subtract another vector component-wise."""
        if not isinstance(other, Vector3):
            return NotImplemented
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Vector3":
        """Scale the vector by a scalar."""
        if not isinstance(scalar, (int, float)):
            raise TypeError("Scalar must be numeric")
        return Vector3(self.x * float(scalar), self.y * float(scalar), self.z * float(scalar))

    def __rmul__(self, scalar: float) -> "Vector3":
        """Support scalar multiplication on the left."""
        return self * scalar

    def __truediv__(self, scalar: float) -> "Vector3":
        """Divide the vector by a scalar."""
        if not isinstance(scalar, (int, float)):
            raise TypeError("Scalar must be numeric")
        if float(scalar) == 0.0:
            raise ZeroDivisionError("Cannot divide a vector by zero")
        return Vector3(self.x / float(scalar), self.y / float(scalar), self.z / float(scalar))

    def __neg__(self) -> "Vector3":
        """Return the additive inverse of the vector."""
        return Vector3(-self.x, -self.y, -self.z)

    def dot(self, other: "Vector3") -> float:
        """Compute the dot product with another vector."""
        if not isinstance(other, Vector3):
            raise TypeError("Expected a Vector3 instance")
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vector3") -> "Vector3":
        """Compute the cross product with another vector."""
        if not isinstance(other, Vector3):
            raise TypeError("Expected a Vector3 instance")
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def magnitude(self) -> float:
        """Return the Euclidean norm of the vector."""
        return math.sqrt(self.squared_magnitude())

    def squared_magnitude(self) -> float:
        """Return the squared Euclidean norm of the vector."""
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalized(self) -> "Vector3":
        """Return a unit vector in the same direction."""
        magnitude = self.magnitude()
        if magnitude == 0.0:
            raise ValueError("Cannot normalize a zero-length vector")
        return self / magnitude

    def distance_to(self, other: "Vector3") -> float:
        """Return the distance to another vector."""
        return (self - other).magnitude()

    def project_onto(self, basis: "Vector3") -> "Vector3":
        """Project the vector onto another vector."""
        if not isinstance(basis, Vector3):
            raise TypeError("Expected a Vector3 instance")
        basis_magnitude = basis.squared_magnitude()
        if basis_magnitude == 0.0:
            raise ValueError("Cannot project onto a zero-length vector")
        scaling = self.dot(basis) / basis_magnitude
        return basis * scaling

    def to_tuple(self) -> tuple[float, float, float]:
        """Return the components as a tuple."""
        return (self.x, self.y, self.z)


@dataclass(slots=True)
class CoordinateSystem:
    """A right-handed coordinate frame with an origin and basis vectors."""

    origin: Vector3
    basis_x: Vector3
    basis_y: Vector3
    basis_z: Vector3

    def __post_init__(self) -> None:
        """Validate the coordinate frame inputs."""
        if not isinstance(self.origin, Vector3):
            raise TypeError("origin must be a Vector3")
        for name, value in (("basis_x", self.basis_x), ("basis_y", self.basis_y), ("basis_z", self.basis_z)):
            if not isinstance(value, Vector3):
                raise TypeError(f"{name} must be a Vector3")

    def to_local(self, point: Vector3) -> Vector3:
        """Convert a global point into coordinates relative to the frame."""
        if not isinstance(point, Vector3):
            raise TypeError("point must be a Vector3")
        offset = point - self.origin
        return Vector3(
            offset.dot(self.basis_x),
            offset.dot(self.basis_y),
            offset.dot(self.basis_z),
        )

    def to_global(self, point: Vector3) -> Vector3:
        """Convert a local point into global coordinates."""
        if not isinstance(point, Vector3):
            raise TypeError("point must be a Vector3")
        return self.origin + self.basis_x * point.x + self.basis_y * point.y + self.basis_z * point.z
