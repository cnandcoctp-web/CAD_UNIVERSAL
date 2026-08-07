"""Pattern feature helpers."""

from __future__ import annotations

from MODELING.body import ModelBody


def apply_pattern(body: ModelBody, parameters: dict[str, object]) -> ModelBody:
    """Apply a simplified feature pattern."""
    count = max(1, int(parameters.get("count", 1)))
    body.volume *= count
    body.face_count *= count
    body.edge_count *= count
    return body
