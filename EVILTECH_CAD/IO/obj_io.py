"""OBJ mesh import/export helpers."""

from __future__ import annotations

from GEOMETRY.mesh import Mesh
from GEOMETRY.point import Point3D


class OBJAdapter:
    """Serialize and deserialize lightweight OBJ meshes."""

    def export_mesh(self, mesh: Mesh) -> str:
        """Export a mesh as Wavefront OBJ text."""
        lines = [f"v {vertex.x} {vertex.y} {vertex.z}" for vertex in mesh.vertices]
        lines.extend("f " + " ".join(str(index + 1) for index in face) for face in mesh.faces)
        return "\n".join(lines)

    def import_mesh(self, payload: str) -> Mesh:
        """Parse Wavefront OBJ text into a mesh."""
        vertices: list[Point3D] = []
        faces: list[tuple[int, ...]] = []
        for line in payload.splitlines():
            if line.startswith("v "):
                _, x_value, y_value, z_value = line.split()
                vertices.append(Point3D(float(x_value), float(y_value), float(z_value)))
            elif line.startswith("f "):
                faces.append(tuple(int(item.split("/")[0]) - 1 for item in line.split()[1:]))
        return Mesh(vertices=vertices, faces=faces)
