"""Interpolation helpers for smooth numerical transitions."""

from __future__ import annotations


def linear_interpolate(start: float, end: float, factor: float) -> float:
    """Linearly interpolate between two values."""
    if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
        raise TypeError("start and end must be numeric")
    if not isinstance(factor, (int, float)):
        raise TypeError("factor must be numeric")
    return float(start) + float(factor) * (float(end) - float(start))


def cubic_interpolate(p0: float, p1: float, p2: float, p3: float, factor: float) -> float:
    """Perform a cubic interpolation between four control points."""
    if not isinstance(p0, (int, float)) or not isinstance(p1, (int, float)) or not isinstance(p2, (int, float)) or not isinstance(p3, (int, float)):
        raise TypeError("interpolation points must be numeric")
    if not isinstance(factor, (int, float)):
        raise TypeError("factor must be numeric")
    factor_value = float(factor)
    return (
        0.5
        * (
            (2.0 * float(p1))
            + (-float(p0) + float(p2)) * factor_value
            + (2.0 * float(p0) - 5.0 * float(p1) + 4.0 * float(p2) - float(p3)) * factor_value * factor_value
            + (-float(p0) + 3.0 * float(p1) - 3.0 * float(p2) + float(p3)) * factor_value * factor_value * factor_value
        )
    )
