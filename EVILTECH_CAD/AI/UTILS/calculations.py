"""Numerical helper functions for the AI pipeline."""

from __future__ import annotations


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    """Clamp a numeric value to a bounded interval."""
    return max(lower, min(upper, value))


def safe_ratio(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Return a safe ratio when the denominator may be zero."""
    if denominator == 0.0:
        return default
    return numerator / denominator


def weighted_average(pairs: list[tuple[float, float]]) -> float:
    """Compute a weighted average from `(value, weight)` pairs."""
    weighted_total = sum(value * weight for value, weight in pairs)
    total_weight = sum(weight for _, weight in pairs)
    return safe_ratio(weighted_total, total_weight, default=0.0)
