"""Geometry kernel package for EvilTech CAD."""

from GEOMETRY.arc import Arc
from GEOMETRY.circle import Circle
from GEOMETRY.intersection import intersect_line_circle, intersect_line_line
from GEOMETRY.line import Line
from GEOMETRY.plane import Plane
from GEOMETRY.point import Point3D
from GEOMETRY.polygon import Polygon
from GEOMETRY.spline import Spline
from GEOMETRY.surface import Surface
from GEOMETRY.topology import BoundingBox, MeshTopology, SolidTopology
from GEOMETRY.transform import GeometricTransform
from GEOMETRY.vector import Vector3D

__all__ = [
    "Arc",
    "Circle",
    "Line",
    "Plane",
    "Point3D",
    "Polygon",
    "Spline",
    "Surface",
    "BoundingBox",
    "MeshTopology",
    "SolidTopology",
    "GeometricTransform",
    "Vector3D",
    "intersect_line_circle",
    "intersect_line_line",
]
