"""Extrude feature helpers."""

from __future__ import annotations

from MODELING.body import ModelBody


def apply_extrude(part: "PartModel", body: ModelBody, parameters: dict[str, object]) -> ModelBody:
    """Apply a simplified extrude operation."""
    sketch = part.sketch_manager.get(str(parameters["sketch"]))
    distance = float(parameters.get("distance", 0.0))
    area = sum(profile.area for profile in sketch.profiles)
    added_volume = area * distance
    if body.body_count == 0 and body.volume == 0.0:
        return ModelBody(name=f"{part.name}-body", volume=added_volume, face_count=6, edge_count=12, body_count=1, metadata={"source": sketch.name})
    body.volume += added_volume
    body.face_count += 2
    body.edge_count += 4
    return body
