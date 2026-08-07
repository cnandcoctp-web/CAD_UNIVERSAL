"""Overlay rendering helpers for selection, highlights, and backgrounds."""

from __future__ import annotations

from dataclasses import dataclass

from GEOMETRY.topology import BoundingBox


@dataclass(slots=True)
class BackgroundSystem:
    """Background rendering configuration."""

    style: str = "solid"
    primary_color: str = "#111827"
    secondary_color: str = "#1f2937"

    def serialize(self) -> dict[str, str]:
        """Return the background configuration."""
        return {
            "style": self.style,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color,
        }


@dataclass(slots=True)
class CoordinateGizmo:
    """A viewport corner coordinate gizmo descriptor."""

    size: int = 48

    def serialize(self) -> dict[str, object]:
        """Return the gizmo configuration."""
        return {
            "size": self.size,
            "axes": ["x", "y", "z"],
        }


class OverlayRenderer:
    """Generate overlay descriptors for highlights, selection, and gizmos."""

    def __init__(self, background: BackgroundSystem | None = None, gizmo: CoordinateGizmo | None = None) -> None:
        self.background = background or BackgroundSystem()
        self.gizmo = gizmo or CoordinateGizmo()

    def render(
        self,
        selection_ids: list[str] | None = None,
        highlighted_ids: list[str] | None = None,
        bounding_boxes: list[BoundingBox] | None = None,
    ) -> dict[str, object]:
        """Return overlay descriptors for the current frame."""
        boxes = [
            {
                "type": "bounding_box",
                "points": [point.to_dict() for point in box.points],
            }
            for box in (bounding_boxes or [])
        ]
        return {
            "background": self.background.serialize(),
            "gizmo": self.gizmo.serialize(),
            "selection": list(selection_ids or []),
            "highlight": list(highlighted_ids or []),
            "bounding_boxes": boxes,
        }
