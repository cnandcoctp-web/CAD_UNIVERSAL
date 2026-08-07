"""Regression tests for the EvilTech CAD geometry kernel."""

from __future__ import annotations

import math

import pytest

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


def test_point_and_vector_operations() -> None:
    point = Point3D(1.0, 2.0, 3.0)
    vector = Vector3D(2.0, 0.0, 0.0)

    moved = point.translate(vector)
    assert moved == Point3D(3.0, 2.0, 3.0)
    assert point.distance_to(Point3D(4.0, 2.0, 3.0)) == 3.0


def test_line_and_plane_interactions() -> None:
    line = Line(Point3D(0.0, 0.0, 0.0), Point3D(2.0, 0.0, 0.0))
    plane = Plane(Point3D(0.0, 0.0, 0.0), Vector3D(0.0, 1.0, 0.0), Vector3D(0.0, 0.0, 1.0))

    assert line.length() == 2.0
    assert plane.contains_point(Point3D(0.0, 5.0, 7.0))


def test_circle_and_arc_measurements() -> None:
    circle = Circle(center=Point3D(0.0, 0.0, 0.0), radius=2.0)
    assert circle.area() == pytest.approx(math.pi * 4.0)
    assert circle.circumference() == pytest.approx(4.0 * math.pi)

    arc = Arc(center=Point3D(0.0, 0.0, 0.0), radius=2.0, start_angle=0.0, end_angle=math.pi / 2.0)
    assert arc.length() == pytest.approx(math.pi)


def test_polygon_and_spline() -> None:
    polygon = Polygon([Point3D(0.0, 0.0, 0.0), Point3D(2.0, 0.0, 0.0), Point3D(2.0, 2.0, 0.0)])
    assert polygon.area() == 2.0
    assert polygon.perimeter() == pytest.approx(4.0 + 2.0 * math.sqrt(2.0))

    spline = Spline([Point3D(0.0, 0.0, 0.0), Point3D(1.0, 1.0, 0.0), Point3D(2.0, 0.0, 0.0)])
    assert len(spline.points) == 3


def test_surface_and_topology() -> None:
    surface = Surface([Point3D(0.0, 0.0, 0.0), Point3D(1.0, 0.0, 0.0), Point3D(1.0, 1.0, 0.0), Point3D(0.0, 1.0, 0.0)])
    assert surface.area() == 1.0

    bbox = BoundingBox([Point3D(0.0, 0.0, 0.0), Point3D(2.0, 3.0, 4.0)])
    assert bbox.volume() == 24.0

    mesh = MeshTopology([Point3D(0.0, 0.0, 0.0), Point3D(1.0, 0.0, 0.0), Point3D(0.0, 1.0, 0.0)])
    assert len(mesh.vertices) == 3

    solid = SolidTopology([Point3D(0.0, 0.0, 0.0), Point3D(1.0, 0.0, 0.0), Point3D(0.0, 1.0, 0.0), Point3D(0.0, 0.0, 1.0)])
    assert len(solid.vertices) == 4


def test_intersections_and_transformations() -> None:
    line = Line(Point3D(0.0, 0.0, 0.0), Point3D(4.0, 0.0, 0.0))
    circle = Circle(center=Point3D(2.0, 0.0, 0.0), radius=1.0)
    intersections = intersect_line_circle(line, circle)
    assert len(intersections) == 2

    line_a = Line(Point3D(0.0, 0.0, 0.0), Point3D(1.0, 1.0, 0.0))
    line_b = Line(Point3D(0.0, 1.0, 0.0), Point3D(1.0, 0.0, 0.0))
    intersection = intersect_line_line(line_a, line_b)
    assert intersection is not None

    transform = GeometricTransform.translation(1.0, 2.0, 3.0)
    point = Point3D(1.0, 1.0, 1.0).transform(transform)
    assert point == Point3D(2.0, 3.0, 4.0)
