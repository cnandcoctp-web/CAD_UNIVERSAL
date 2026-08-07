"""Intersection and spatial-query helpers for the EvilTech CAD geometry kernel."""

from __future__ import annotations

import math

from GEOMETRY.circle import Circle
from GEOMETRY.line import Line
from GEOMETRY.point import Point3D


def intersect_line_line(line_a: Line, line_b: Line) -> Point3D | None:
    """Return the intersection point of two lines if one exists."""
    if not isinstance(line_a, Line) or not isinstance(line_b, Line):
        raise TypeError("line arguments must be Line instances")
    x1, y1 = line_a.start.x, line_a.start.y
    x2, y2 = line_a.end.x, line_a.end.y
    x3, y3 = line_b.start.x, line_b.start.y
    x4, y4 = line_b.end.x, line_b.end.y

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denominator) < 1e-9:
        return None
    numerator = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4))
    x = numerator / denominator
    y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator
    return Point3D(x, y, 0.0)


def intersect_line_circle(line: Line, circle: Circle) -> list[Point3D]:
    """Return the intersection points between a line and a circle."""
    if not isinstance(line, Line) or not isinstance(circle, Circle):
        raise TypeError("line and circle arguments must be valid geometry objects")
    dx = line.end.x - line.start.x
    dy = line.end.y - line.start.y
    fx = line.start.x - circle.center.x
    fy = line.start.y - circle.center.y
    a = dx * dx + dy * dy
    b = 2.0 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - circle.radius * circle.radius
    discriminant = b * b - 4.0 * a * c
    if discriminant < 0.0:
        return []
    if abs(discriminant) < 1e-9:
        t = -b / (2.0 * a)
        return [Point3D(line.start.x + t * dx, line.start.y + t * dy, 0.0)]
    sqrt_discriminant = math.sqrt(discriminant)
    t1 = (-b - sqrt_discriminant) / (2.0 * a)
    t2 = (-b + sqrt_discriminant) / (2.0 * a)
    return [Point3D(line.start.x + t1 * dx, line.start.y + t1 * dy, 0.0), Point3D(line.start.x + t2 * dx, line.start.y + t2 * dy, 0.0)]
