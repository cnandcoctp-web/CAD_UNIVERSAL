"""Dimensional constraint application helpers."""

from __future__ import annotations

import math

from CONSTRAINTS.constraint_registry import Constraint, ConstraintType
from CONSTRAINTS.tolerance_constraints import ConstraintTolerance
from GEOMETRY.circle import Circle
from GEOMETRY.line import Line
from GEOMETRY.point import Point3D


def _set_point(point: Point3D, x: float, y: float) -> None:
    point.x = float(x)
    point.y = float(y)


def evaluate_dimensional(constraint: Constraint, entities: dict[str, object], tolerance: ConstraintTolerance) -> float:
    """Return the current residual for a dimensional constraint."""
    if constraint.constraint_type == ConstraintType.DISTANCE:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        return abs(math.dist((first.x, first.y), (second.x, second.y)) - float(constraint.value or 0.0))
    if constraint.constraint_type == ConstraintType.ANGLE:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        angle = _line_angle_between(first, second)
        return abs(angle - float(constraint.value or 0.0))
    if constraint.constraint_type == ConstraintType.RADIUS:
        circle = entities[constraint.entity_ids[0]]
        return abs(circle.radius - float(constraint.value or 0.0))
    if constraint.constraint_type == ConstraintType.DIAMETER:
        circle = entities[constraint.entity_ids[0]]
        return abs(circle.radius * 2.0 - float(constraint.value or 0.0))
    return 0.0


def apply_dimensional(constraint: Constraint, entities: dict[str, object], tolerance: ConstraintTolerance) -> float:
    """Apply a single dimensional constraint and return its resulting residual."""
    if constraint.constraint_type == ConstraintType.DISTANCE:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        target = float(constraint.value or 0.0)
        dx = second.x - first.x
        dy = second.y - first.y
        current = math.hypot(dx, dy)
        if current == 0.0:
            _set_point(second, first.x + target, first.y)
        else:
            scale = target / current
            _set_point(second, first.x + dx * scale, first.y + dy * scale)
    elif constraint.constraint_type == ConstraintType.ANGLE:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        target = math.radians(float(constraint.value or 0.0))
        first_angle = math.atan2(first.end.y - first.start.y, first.end.x - first.start.x)
        desired = first_angle + target
        length = math.hypot(second.end.x - second.start.x, second.end.y - second.start.y)
        _set_point(second.end, second.start.x + math.cos(desired) * length, second.start.y + math.sin(desired) * length)
    elif constraint.constraint_type == ConstraintType.RADIUS:
        circle = entities[constraint.entity_ids[0]]
        circle.radius = float(constraint.value or 0.0)
    elif constraint.constraint_type == ConstraintType.DIAMETER:
        circle = entities[constraint.entity_ids[0]]
        circle.radius = float(constraint.value or 0.0) / 2.0
    return evaluate_dimensional(constraint, entities, tolerance)


def _line_angle_between(first: Line, second: Line) -> float:
    angle1 = math.atan2(first.end.y - first.start.y, first.end.x - first.start.x)
    angle2 = math.atan2(second.end.y - second.start.y, second.end.x - second.start.x)
    delta = abs(math.degrees(angle2 - angle1)) % 360.0
    if delta > 180.0:
        delta = 360.0 - delta
    return delta
