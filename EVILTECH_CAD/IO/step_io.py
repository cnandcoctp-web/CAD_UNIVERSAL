"""STEP-style solid import/export helpers."""

from __future__ import annotations

from GEOMETRY.point import Point3D
from GEOMETRY.solid import Solid


class STEPAdapter:
    """Serialize and deserialize lightweight STEP-like solids."""

    def export_solid(self, solid: Solid) -> str:
        """Export a solid to a simplified STEP-like text block."""
        lines = ["ISO-10303-21;", f"/* {solid.name} */"]
        lines.extend(f"CARTESIAN_POINT('',({vertex.x},{vertex.y},{vertex.z}));" for vertex in solid.vertices)
        lines.append("END-ISO-10303-21;")
        return "\n".join(lines)

    def import_solid(self, payload: str, name: str = "Imported STEP") -> Solid:
        """Parse a simplified STEP-like text block."""
        vertices: list[Point3D] = []
        for line in payload.splitlines():
            if "CARTESIAN_POINT" not in line:
                continue
            chunk = line.split("(", 2)[2].split(")", 1)[0]
            x_value, y_value, z_value = (float(value.strip()) for value in chunk.split(","))
            vertices.append(Point3D(x_value, y_value, z_value))
        return Solid(name=name, vertices=vertices)
