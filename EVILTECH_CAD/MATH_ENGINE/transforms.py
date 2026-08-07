"""Transformation utilities for affine transforms and coordinate mapping."""

from __future__ import annotations

import math
from dataclasses import dataclass

from MATH_ENGINE.algebra import Vector3
from MATH_ENGINE.matrix import Matrix


@dataclass(slots=True)
class Transform:
    """An affine transform expressed as a homogeneous 4x4 matrix."""

    matrix: Matrix

    def __post_init__(self) -> None:
        """Validate that the stored matrix is a 4x4 homogeneous transform."""
        if not isinstance(self.matrix, Matrix):
            raise TypeError("matrix must be a Matrix instance")
        if self.matrix.rows != 4 or self.matrix.cols != 4:
            raise ValueError("Transform matrices must be 4x4")

    @classmethod
    def translation(cls, tx: float, ty: float, tz: float) -> "Transform":
        """Create a translation transform."""
        return cls(Matrix([[1.0, 0.0, 0.0, tx], [0.0, 1.0, 0.0, ty], [0.0, 0.0, 1.0, tz], [0.0, 0.0, 0.0, 1.0]]))

    @classmethod
    def rotation_x(cls, angle: float) -> "Transform":
        """Create a rotation transform around the x-axis."""
        cosine = math.cos(angle)
        sine = math.sin(angle)
        return cls(Matrix([[1.0, 0.0, 0.0, 0.0], [0.0, cosine, -sine, 0.0], [0.0, sine, cosine, 0.0], [0.0, 0.0, 0.0, 1.0]]))

    @classmethod
    def rotation_y(cls, angle: float) -> "Transform":
        """Create a rotation transform around the y-axis."""
        cosine = math.cos(angle)
        sine = math.sin(angle)
        return cls(Matrix([[cosine, 0.0, sine, 0.0], [0.0, 1.0, 0.0, 0.0], [-sine, 0.0, cosine, 0.0], [0.0, 0.0, 0.0, 1.0]]))

    @classmethod
    def rotation_z(cls, angle: float) -> "Transform":
        """Create a rotation transform around the z-axis."""
        cosine = math.cos(angle)
        sine = math.sin(angle)
        return cls(Matrix([[cosine, -sine, 0.0, 0.0], [sine, cosine, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]))

    @classmethod
    def scale(cls, sx: float, sy: float, sz: float) -> "Transform":
        """Create a scale transform."""
        return cls(Matrix([[sx, 0.0, 0.0, 0.0], [0.0, sy, 0.0, 0.0], [0.0, 0.0, sz, 0.0], [0.0, 0.0, 0.0, 1.0]]))

    def __mul__(self, other: object) -> "Transform":
        """Compose this transform with another transform."""
        if not isinstance(other, Transform):
            raise TypeError("Expected a Transform instance")
        return Transform(other.matrix * self.matrix)

    def transform_point(self, point: Vector3) -> Vector3:
        """Transform a point as a position in space."""
        if not isinstance(point, Vector3):
            raise TypeError("point must be a Vector3")
        values = [point.x, point.y, point.z, 1.0]
        transformed = [sum(self.matrix.data[row][column] * values[column] for column in range(4)) for row in range(4)]
        return Vector3(transformed[0], transformed[1], transformed[2])

    def transform_vector(self, vector: Vector3) -> Vector3:
        """Transform a vector without applying translation."""
        if not isinstance(vector, Vector3):
            raise TypeError("vector must be a Vector3")
        values = [vector.x, vector.y, vector.z, 0.0]
        transformed = [sum(self.matrix.data[row][column] * values[column] for column in range(4)) for row in range(4)]
        return Vector3(transformed[0], transformed[1], transformed[2])
