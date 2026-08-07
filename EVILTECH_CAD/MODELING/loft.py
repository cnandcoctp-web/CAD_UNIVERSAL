"""Loft feature helpers."""

from __future__ import annotations

from MODELING.body import ModelBody


def apply_loft(part: "PartModel", body: ModelBody, parameters: dict[str, object]) -> ModelBody:
    """Apply a simplified loft operation."""
    profiles = [part.sketch_manager.get(name) for name in parameters.get("profiles", [])]
    length = float(parameters.get("length", 0.0))
    areas = [sum(profile.area for profile in sketch.profiles) for sketch in profiles]
    average_area = sum(areas) / max(1, len(areas))
    body.volume += average_area * length
    body.face_count += 5
    body.edge_count += 10
    body.body_count = max(1, body.body_count)
    return body
