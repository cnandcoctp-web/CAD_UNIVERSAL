"""Nonlinear equation solvers for the mathematical engine."""

from __future__ import annotations

import math
from typing import Callable


class NewtonRaphsonSolver:
    """A Newton-Raphson solver for scalar nonlinear equations."""

    def __init__(self, tolerance: float = 1e-8, max_iterations: int = 50) -> None:
        """Initialize the solver with convergence parameters."""
        if not isinstance(tolerance, (int, float)):
            raise TypeError("tolerance must be numeric")
        if not isinstance(max_iterations, int) or max_iterations <= 0:
            raise ValueError("max_iterations must be a positive integer")
        self.tolerance = float(tolerance)
        self.max_iterations = max_iterations

    def solve(self, function: Callable[[float], float], initial_guess: float) -> float:
        """Solve f(x) = 0 starting from the initial guess."""
        if not callable(function):
            raise TypeError("function must be callable")
        if not isinstance(initial_guess, (int, float)):
            raise TypeError("initial_guess must be numeric")

        current = float(initial_guess)
        for _ in range(self.max_iterations):
            value = function(current)
            if abs(value) <= self.tolerance:
                return current
            derivative = self._finite_difference_derivative(function, current)
            if derivative == 0.0:
                raise ValueError("Newton-Raphson derivative is zero")
            next_value = current - value / derivative
            if abs(next_value - current) <= self.tolerance:
                return next_value
            current = next_value
        raise RuntimeError("Newton-Raphson solver did not converge")

    @staticmethod
    def _finite_difference_derivative(function: Callable[[float], float], point: float) -> float:
        """Estimate the derivative numerically using a small offset."""
        step = 1e-6
        return (function(point + step) - function(point - step)) / (2.0 * step)
