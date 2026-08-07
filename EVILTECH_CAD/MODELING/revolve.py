"""Revolve feature helpers."""

from __future__ import annotations

from math import pi

from MODELING.body import ModelBody


def apply_revolve(part: "PartModel", body: ModelBody, parameters: dict[str, object]) -> ModelBody:
    """Apply a simplified revolve operation."""
    sketch = part.sketch_manager.get(str(parameters["sketch"]))
    angle = float(parameters.get("angle", 360.0)) / 360.0
    radius = float(parameters.get("radius", 1.0))
    area = sum(profile.area for profile in sketch.profiles)
    added_volume = area * 2.0 * pi * radius * angle
    if body.body_count == 0 and body.volume == 0.0:
        return ModelBody(name=f"{part.name}-body", volume=added_volume, face_count=8, edge_count=16, body_count=1, metadata={"source": sketch.name})
    body.volume += added_volume
    body.face_count += 4
    body.edge_count += 8
    return body
