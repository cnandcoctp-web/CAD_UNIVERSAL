"""Section-analysis tools for EvilTech CAD."""

from __future__ import annotations

from GEOMETRY.solid import Solid


def section_summary(solid: Solid, axis: str = "z") -> dict[str, float | str]:
    """Return a lightweight section summary for a solid."""
    bounds = solid.bounding_box()
    points = bounds.points
    spans = {
        "x": max(point.x for point in points) - min(point.x for point in points),
        "y": max(point.y for point in points) - min(point.y for point in points),
        "z": max(point.z for point in points) - min(point.z for point in points),
    }
    return {"axis": axis.lower(), "span": spans[axis.lower()], "volume": solid.volume()}
