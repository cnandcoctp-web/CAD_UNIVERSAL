"""Precision and tolerance utilities for comparing floating-point values."""

from __future__ import annotations

import math


class Tolerance:
    """A reusable tolerance class for numerical comparisons."""

    def __init__(self, absolute: float = 1e-6, relative: float = 1e-6) -> None:
        """Initialize the tolerance with absolute and relative bounds."""
        if not isinstance(absolute, (int, float)):
            raise TypeError("absolute must be numeric")
        if not isinstance(relative, (int, float)):
            raise TypeError("relative must be numeric")
        self.absolute = float(absolute)
        self.relative = float(relative)

    def is_close(self, left: float, right: float) -> bool:
        """Determine whether two values are close within the configured tolerance."""
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise TypeError("left and right must be numeric")
        difference = abs(float(left) - float(right))
        scale = max(abs(float(left)), abs(float(right)), 1.0)
        return difference <= max(self.absolute, self.relative * scale)


def is_close(left: float, right: float, absolute: float = 1e-6, relative: float = 1e-6) -> bool:
    """Convenience function for comparing floating-point values."""
    return Tolerance(absolute=absolute, relative=relative).is_close(left, right)
