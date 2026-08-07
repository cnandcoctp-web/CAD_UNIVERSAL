"""Shell feature helpers."""

from __future__ import annotations

from MODELING.body import ModelBody


def apply_shell(body: ModelBody, parameters: dict[str, object]) -> ModelBody:
    """Apply a simplified shell operation."""
    thickness = float(parameters.get("thickness", 0.0))
    body.volume *= max(0.1, 1.0 - thickness * 0.1)
    body.face_count += 1
    return body
