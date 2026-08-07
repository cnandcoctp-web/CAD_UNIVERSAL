"""General mathematical utility helpers used throughout the engine."""

from __future__ import annotations

import math


def clamp(value: float, lower: float, upper: float) -> float:
    """Clamp a numeric value to the inclusive range [lower, upper]."""
    if not isinstance(value, (int, float)):
        raise TypeError("value must be numeric")
    if not isinstance(lower, (int, float)):
        raise TypeError("lower must be numeric")
    if not isinstance(upper, (int, float)):
        raise TypeError("upper must be numeric")
    if lower > upper:
        raise ValueError("lower bound must be less than or equal to upper bound")
    return max(lower, min(upper, float(value)))


def ensure_finite(value: float, default: float = 0.0) -> float:
    """Return a finite float, falling back to a default when needed."""
    if not isinstance(value, (int, float)):
        raise TypeError("value must be numeric")
    numeric = float(value)
    if math.isfinite(numeric):
        return numeric
    return float(default)


def normalize_angle(angle: float) -> float:
    """Normalize an angle to the interval [0, 2π)."""
    if not isinstance(angle, (int, float)):
        raise TypeError("angle must be numeric")
    normalized = float(angle) % (2.0 * math.pi)
    if normalized < 0.0:
        normalized += 2.0 * math.pi
    return normalized


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two values and return a fallback on division by zero."""
    if not isinstance(numerator, (int, float)):
        raise TypeError("numerator must be numeric")
    if not isinstance(denominator, (int, float)):
        raise TypeError("denominator must be numeric")
    if float(denominator) == 0.0:
        return float(default)
    return float(numerator) / float(denominator)
