"""Fillet tool for lightweight model bodies."""

from __future__ import annotations

from MODELING.feature import ModelBody


def apply_fillet(body: ModelBody, radius: float, edge_count: int = 1) -> ModelBody:
    """Apply a lightweight fillet approximation to a body."""
    updated = body.clone(name=f"{body.name}-fillet")
    updated.volume = max(0.0, updated.volume - abs(radius) * max(1, edge_count) * 0.5)
    updated.face_count += max(1, edge_count)
    return updated
