"""IGES-style solid import/export helpers."""

from __future__ import annotations

from GEOMETRY.point import Point3D
from GEOMETRY.solid import Solid


class IGESAdapter:
    """Serialize and deserialize lightweight IGES-like solids."""

    def export_solid(self, solid: Solid) -> str:
        """Export a solid as a simple IGES-style coordinate list."""
        lines = [f"IGES_SOLID {solid.name}"]
        lines.extend(f"VERTEX {vertex.x} {vertex.y} {vertex.z}" for vertex in solid.vertices)
        return "\n".join(lines)

    def import_solid(self, payload: str) -> Solid:
        """Parse a simple IGES-style coordinate list."""
        lines = payload.splitlines()
        name = lines[0].split(maxsplit=1)[1]
        vertices = [Point3D(*map(float, line.split()[1:4])) for line in lines[1:] if line.startswith("VERTEX ")]
        return Solid(name=name, vertices=vertices)
