"""Matrix mathematics and linear algebra helpers for EvilTech CAD."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Iterator, Sequence

from MATH_ENGINE.algebra import Vector3


@dataclass(slots=True)
class Matrix:
    """A dense matrix supporting arithmetic and linear algebra operations."""

    data: list[list[float]]
    _rows: int = field(init=False, repr=False)
    _cols: int = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Validate the matrix structure and values."""
        if not self.data:
            raise ValueError("Matrix must contain at least one row")
        rows = len(self.data)
        width = len(self.data[0])
        if width == 0:
            raise ValueError("Matrix rows must not be empty")
        for row in self.data:
            if len(row) != width:
                raise ValueError("Matrix rows must all have the same length")
            for index, value in enumerate(row):
                if not isinstance(value, (int, float)):
                    raise TypeError(f"Matrix element at ({rows}, {index}) must be numeric")
                if not math.isfinite(float(value)):
                    raise ValueError(f"Matrix element at ({rows}, {index}) must be finite")
        self._rows = rows
        self._cols = width

    @property
    def rows(self) -> int:
        """Return the number of rows in the matrix."""
        return self._rows

    @property
    def cols(self) -> int:
        """Return the number of columns in the matrix."""
        return self._cols

    def __iter__(self) -> Iterator[list[float]]:
        """Yield each row as a list."""
        yield from self.data

    def __len__(self) -> int:
        """Return the number of rows in the matrix."""
        return self.rows

    def __getitem__(self, index: int) -> list[float]:
        """Access a row by index."""
        return self.data[index]

    def __eq__(self, other: object) -> bool:
        """Compare two matrices by their values and dimensions."""
        if not isinstance(other, Matrix):
            return NotImplemented
        return self.data == other.data

    def __add__(self, other: "Matrix") -> "Matrix":
        """Add two matrices component-wise."""
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition")
        return Matrix([[self.data[r][c] + other.data[r][c] for c in range(self.cols)] for r in range(self.rows)])

    def __sub__(self, other: "Matrix") -> "Matrix":
        """Subtract one matrix from another component-wise."""
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction")
        return Matrix([[self.data[r][c] - other.data[r][c] for c in range(self.cols)] for r in range(self.rows)])

    def __mul__(self, other: object) -> object:
        """Multiply the matrix by another matrix, vector, scalar, or sequence."""
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError("Matrix dimensions are incompatible for multiplication")
            return Matrix(
                [
                    [sum(self.data[r][k] * other.data[k][c] for k in range(self.cols)) for c in range(other.cols)]
                    for r in range(self.rows)
                ]
            )
        if isinstance(other, Vector3):
            if self.cols != 3:
                raise ValueError("Matrix-vector multiplication requires a 3-column matrix")
            return Vector3(
                sum(self.data[0][k] * other[k] for k in range(3)),
                sum(self.data[1][k] * other[k] for k in range(3)),
                sum(self.data[2][k] * other[k] for k in range(3)),
            )
        if isinstance(other, Sequence) and not isinstance(other, (str, bytes)):
            values = list(other)
            if len(values) != self.cols:
                raise ValueError("Matrix-by-sequence multiplication requires a compatible dimension")
            return [sum(self.data[r][k] * values[k] for k in range(self.cols)) for r in range(self.rows)]
        if isinstance(other, (int, float)):
            scalar = float(other)
            return Matrix([[scalar * value for value in row] for row in self.data])
        return NotImplemented

    def __rmul__(self, other: object) -> object:
        """Support scalar multiplication on the left."""
        if isinstance(other, (int, float)):
            return self * other
        return NotImplemented

    def transpose(self) -> "Matrix":
        """Return the transpose of the matrix."""
        return Matrix([[self.data[r][c] for r in range(self.rows)] for c in range(self.cols)])

    def determinant(self) -> float:
        """Return the determinant of the matrix using Gaussian elimination."""
        if self.rows != self.cols:
            raise ValueError("Determinant is only defined for square matrices")
        if self.rows == 1:
            return float(self.data[0][0])
        if self.rows == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]

        work = [row[:] for row in self.data]
        determinant = 1.0
        for pivot_index in range(self.rows):
            pivot_row = max(range(pivot_index, self.rows), key=lambda row: abs(work[row][pivot_index]))
            if abs(work[pivot_row][pivot_index]) < 1e-12:
                return 0.0
            if pivot_row != pivot_index:
                work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
                determinant = -determinant
            pivot_value = work[pivot_index][pivot_index]
            determinant *= pivot_value
            for row in range(pivot_index + 1, self.rows):
                factor = work[row][pivot_index] / pivot_value
                for column in range(pivot_index, self.rows):
                    work[row][column] -= factor * work[pivot_index][column]
        return determinant

    def inverse(self) -> "Matrix":
        """Return the inverse of the matrix via Gauss-Jordan elimination."""
        if self.rows != self.cols:
            raise ValueError("Inverse is only defined for square matrices")
        if abs(self.determinant()) < 1e-12:
            raise ValueError("Matrix is singular and cannot be inverted")

        work = [row[:] + [1.0 if index == column else 0.0 for index in range(self.rows)] for column, row in enumerate(self.data)]

        for pivot_index in range(self.rows):
            pivot_row = max(range(pivot_index, self.rows), key=lambda row: abs(work[row][pivot_index]))
            if abs(work[pivot_row][pivot_index]) < 1e-12:
                raise ValueError("Matrix is singular and cannot be inverted")
            if pivot_row != pivot_index:
                work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
            pivot_value = work[pivot_index][pivot_index]
            for column in range(pivot_index, 2 * self.rows):
                work[pivot_index][column] /= pivot_value
            for row in range(self.rows):
                if row == pivot_index:
                    continue
                factor = work[row][pivot_index]
                if factor == 0.0:
                    continue
                for column in range(pivot_index, 2 * self.rows):
                    work[row][column] -= factor * work[pivot_index][column]

        return Matrix([row[self.rows :] for row in work])
