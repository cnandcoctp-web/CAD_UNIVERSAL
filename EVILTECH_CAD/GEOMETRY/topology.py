"""Topology containers for the EvilTech CAD geometry kernel."""

from __future__ import annotations

from dataclasses import dataclass

from GEOMETRY.point import Point3D


@dataclass(slots=True)
class BoundingBox:
    """An axis-aligned bounding box defined by corner points."""

    points: list[Point3D]

    def __post_init__(self) -> None:
        """Validate the bounding box points."""
        if len(self.points) < 2:
            raise ValueError("BoundingBox requires at least two points")
        for point in self.points:
            if not isinstance(point, Point3D):
                raise TypeError("All bounding box points must be Point3D instances")

    def volume(self) -> float:
        """Return the axis-aligned volume of the bounding box."""
        span_x = max(point.x for point in self.points) - min(point.x for point in self.points)
        span_y = max(point.y for point in self.points) - min(point.y for point in self.points)
        span_z = max(point.z for point in self.points) - min(point.z for point in self.points)
        return span_x * span_y * span_z

    def to_dict(self) -> dict[str, object]:
        """Serialize the bounding box to a dictionary."""
        return {"points": [point.to_dict() for point in self.points]}


@dataclass(slots=True)
class MeshTopology:
    """A lightweight mesh topology container."""

    vertices: list[Point3D]

    def __post_init__(self) -> None:
        """Validate the mesh vertices."""
        if not self.vertices:
            raise ValueError("MeshTopology requires at least one vertex")
        for point in self.vertices:
            if not isinstance(point, Point3D):
                raise TypeError("MeshTopology vertices must be Point3D instances")

    def to_dict(self) -> dict[str, object]:
        """Serialize the mesh topology to a dictionary."""
        return {"vertices": [point.to_dict() for point in self.vertices]}


@dataclass(slots=True)
class SolidTopology:
    """A lightweight solid topology container."""

    vertices: list[Point3D]

    def __post_init__(self) -> None:
        """Validate the solid vertices."""
        if not self.vertices:
            raise ValueError("SolidTopology requires at least one vertex")
        for point in self.vertices:
            if not isinstance(point, Point3D):
                raise TypeError("SolidTopology vertices must be Point3D instances")

    def to_dict(self) -> dict[str, object]:
        """Serialize the solid topology to a dictionary."""
        return {"vertices": [point.to_dict() for point in self.vertices]}
