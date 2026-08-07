"""Measurement tools for EvilTech CAD."""

from __future__ import annotations

from GEOMETRY.mesh import Mesh
from GEOMETRY.point import Point3D
from GEOMETRY.solid import Solid
from MODELING.feature import ModelBody


class MeasurementService:
    """Perform common measurement queries."""

    def distance(self, first: Point3D, second: Point3D) -> float:
        """Measure the distance between two points."""
        return first.distance_to(second)

    def volume(self, subject: Solid | ModelBody) -> float:
        """Measure the volume of a solid-like object."""
        if isinstance(subject, Solid):
            return subject.volume()
        if isinstance(subject, ModelBody):
            return subject.volume
        raise TypeError("subject must be a Solid or ModelBody")

    def mesh_summary(self, mesh: Mesh) -> dict[str, int]:
        """Return face and vertex counts for a mesh."""
        return {"vertices": len(mesh.vertices), "faces": mesh.face_count()}
