"""Numerical utilities for differentiation, integration, and linear systems."""

from __future__ import annotations

import math
from typing import Callable

from MATH_ENGINE.matrix import Matrix


def solve_linear_system(matrix: Matrix, vector: list[float]) -> list[float]:
    """Solve a linear system using Gaussian elimination."""
    if not isinstance(matrix, Matrix):
        raise TypeError("matrix must be a Matrix instance")
    if matrix.rows != matrix.cols:
        raise ValueError("A square matrix is required for linear-system solving")
    if len(vector) != matrix.rows:
        raise ValueError("The RHS vector must match the matrix dimension")
    if any(not isinstance(value, (int, float)) for value in vector):
        raise TypeError("vector values must be numeric")

    augmented = [list(row) + [vector[index]] for index, row in enumerate(matrix.data)]
    work = [row[:] for row in augmented]

    for pivot_index in range(matrix.rows):
        pivot_row = max(range(pivot_index, matrix.rows), key=lambda row: abs(work[row][pivot_index]))
        if abs(work[pivot_row][pivot_index]) < 1e-12:
            raise ValueError("The linear system is singular")
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
        pivot_value = work[pivot_index][pivot_index]
        for column in range(pivot_index, matrix.cols + 1):
            work[pivot_index][column] /= pivot_value
        for row in range(matrix.rows):
            if row == pivot_index:
                continue
            factor = work[row][pivot_index]
            if factor == 0.0:
                continue
            for column in range(pivot_index, matrix.cols + 1):
                work[row][column] -= factor * work[pivot_index][column]

    return [work[row][matrix.cols] for row in range(matrix.rows)]


def estimate_derivative(function: Callable[[float], float], point: float, h: float = 1e-5) -> float:
    """Estimate the derivative of a function at a point using central differences."""
    if not callable(function):
        raise TypeError("function must be callable")
    if not isinstance(point, (int, float)):
        raise TypeError("point must be numeric")
    if not isinstance(h, (int, float)):
        raise TypeError("h must be numeric")
    if float(h) == 0.0:
        raise ValueError("h must be non-zero")
    offset = float(h)
    return (function(point + offset) - function(point - offset)) / (2.0 * offset)


def estimate_integral(function: Callable[[float], float], start: float, end: float, steps: int = 100) -> float:
    """Estimate the definite integral with the trapezoidal rule."""
    if not callable(function):
        raise TypeError("function must be callable")
    if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
        raise TypeError("start and end must be numeric")
    if not isinstance(steps, int) or steps <= 0:
        raise ValueError("steps must be a positive integer")
    left = float(start)
    right = float(end)
    if right < left:
        raise ValueError("end must be greater than or equal to start")
    step = (right - left) / steps
    total = 0.0
    for index in range(steps):
        x0 = left + index * step
        x1 = x0 + step
        total += 0.5 * (function(x0) + function(x1)) * step
    return total
