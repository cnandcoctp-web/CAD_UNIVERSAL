"""STL mesh import/export helpers."""

from __future__ import annotations

from GEOMETRY.mesh import Mesh
from GEOMETRY.point import Point3D


class STLAdapter:
    """Serialize and deserialize lightweight ASCII STL meshes."""

    def export_mesh(self, mesh: Mesh, name: str = "mesh") -> str:
        """Export a mesh to an ASCII STL-like representation."""
        lines = [f"solid {name}"]
        for face in mesh.faces:
            if len(face) < 3:
                continue
            lines.extend(["facet normal 0 0 0", "outer loop"])
            for index in face[:3]:
                vertex = mesh.vertices[index]
                lines.append(f"vertex {vertex.x} {vertex.y} {vertex.z}")
            lines.extend(["endloop", "endfacet"])
        lines.append(f"endsolid {name}")
        return "\n".join(lines)

    def import_mesh(self, payload: str) -> Mesh:
        """Parse a minimal ASCII STL mesh."""
        vertices: list[Point3D] = []
        faces: list[tuple[int, int, int]] = []
        current_face: list[int] = []
        for line in payload.splitlines():
            if line.strip().startswith("vertex "):
                _, x_value, y_value, z_value = line.split()
                vertices.append(Point3D(float(x_value), float(y_value), float(z_value)))
                current_face.append(len(vertices) - 1)
                if len(current_face) == 3:
                    faces.append(tuple(current_face))
                    current_face = []
        return Mesh(vertices=vertices, faces=faces)
