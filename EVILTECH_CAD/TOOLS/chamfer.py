"""Chamfer tool for lightweight model bodies."""

from __future__ import annotations

from MODELING.feature import ModelBody


def apply_chamfer(body: ModelBody, distance: float, edge_count: int = 1) -> ModelBody:
    """Apply a lightweight chamfer approximation to a body."""
    updated = body.clone(name=f"{body.name}-chamfer")
    updated.volume = max(0.0, updated.volume - abs(distance) * max(1, edge_count))
    updated.face_count += max(1, edge_count)
    return updated
