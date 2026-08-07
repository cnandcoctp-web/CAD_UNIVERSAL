"""Sweep feature helpers."""

from __future__ import annotations

from MODELING.body import ModelBody


def apply_sweep(part: "PartModel", body: ModelBody, parameters: dict[str, object]) -> ModelBody:
    """Apply a simplified sweep operation."""
    sketch = part.sketch_manager.get(str(parameters["sketch"]))
    length = float(parameters.get("length", 0.0))
    area = sum(profile.area for profile in sketch.profiles)
    added_volume = area * length
    body.volume += added_volume
    body.face_count += 3
    body.edge_count += 6
    body.body_count = max(1, body.body_count)
    return body
