"""DXF-style polyline import/export helpers."""

from __future__ import annotations

from GEOMETRY.mesh import Mesh
from GEOMETRY.point import Point3D


class DXFAdapter:
    """Serialize and deserialize lightweight DXF-like polylines."""

    def export_mesh(self, mesh: Mesh) -> str:
        """Export a mesh as DXF-style vertex rows."""
        lines = ["0", "SECTION", "2", "ENTITIES"]
        for vertex in mesh.vertices:
            lines.extend(["0", "VERTEX", "10", str(vertex.x), "20", str(vertex.y), "30", str(vertex.z)])
        lines.extend(["0", "ENDSEC", "0", "EOF"])
        return "\n".join(lines)

    def import_mesh(self, payload: str) -> Mesh:
        """Parse DXF-style vertex rows into a mesh."""
        tokens = payload.splitlines()
        vertices: list[Point3D] = []
        for index, token in enumerate(tokens):
            if token == "VERTEX":
                x = float(tokens[index + 2])
                y = float(tokens[index + 4])
                z = float(tokens[index + 6])
                vertices.append(Point3D(x, y, z))
        return Mesh(vertices=vertices, faces=[])
