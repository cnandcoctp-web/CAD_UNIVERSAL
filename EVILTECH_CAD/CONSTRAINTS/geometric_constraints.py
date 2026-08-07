"""Geometric constraint application helpers."""

from __future__ import annotations

import math

from CONSTRAINTS.constraint_registry import Constraint, ConstraintType
from CONSTRAINTS.tolerance_constraints import ConstraintTolerance
from GEOMETRY.circle import Circle
from GEOMETRY.line import Line
from GEOMETRY.point import Point3D


def _set_point(point: Point3D, x: float, y: float, z: float | None = None) -> None:
    point.x = float(x)
    point.y = float(y)
    point.z = point.z if z is None else float(z)


def _line_direction(line: Line) -> tuple[float, float]:
    return (line.end.x - line.start.x, line.end.y - line.start.y)


def _normalize(dx: float, dy: float) -> tuple[float, float]:
    length = math.hypot(dx, dy)
    if length == 0.0:
        return (1.0, 0.0)
    return (dx / length, dy / length)


def _line_length(line: Line) -> float:
    return math.hypot(line.end.x - line.start.x, line.end.y - line.start.y)


def evaluate_geometric(constraint: Constraint, entities: dict[str, object], tolerance: ConstraintTolerance) -> float:
    """Return the current residual for a geometric constraint."""
    if constraint.constraint_type == ConstraintType.COINCIDENT:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        return math.dist((first.x, first.y), (second.x, second.y))
    if constraint.constraint_type == ConstraintType.HORIZONTAL:
        entity = entities[constraint.entity_ids[0]]
        if isinstance(entity, Line):
            return abs(entity.end.y - entity.start.y)
    if constraint.constraint_type == ConstraintType.VERTICAL:
        entity = entities[constraint.entity_ids[0]]
        if isinstance(entity, Line):
            return abs(entity.end.x - entity.start.x)
    if constraint.constraint_type == ConstraintType.PARALLEL:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        dx1, dy1 = _normalize(*_line_direction(first))
        dx2, dy2 = _normalize(*_line_direction(second))
        return abs(dx1 * dy2 - dy1 * dx2)
    if constraint.constraint_type == ConstraintType.PERPENDICULAR:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        dx1, dy1 = _normalize(*_line_direction(first))
        dx2, dy2 = _normalize(*_line_direction(second))
        return abs(dx1 * dx2 + dy1 * dy2)
    if constraint.constraint_type == ConstraintType.CONCENTRIC:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        return math.dist((first.center.x, first.center.y), (second.center.x, second.center.y))
    if constraint.constraint_type == ConstraintType.TANGENT:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        if isinstance(first, Line) and isinstance(second, Circle):
            return abs(_distance_point_to_line(second.center, first) - second.radius)
    if constraint.constraint_type == ConstraintType.EQUAL_LENGTH:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        return abs(_line_length(first) - _line_length(second))
    if constraint.constraint_type == ConstraintType.EQUAL_RADIUS:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        return abs(first.radius - second.radius)
    if constraint.constraint_type == ConstraintType.SYMMETRY:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        center = entities[constraint.entity_ids[2]]
        midpoint_x = (first.x + second.x) / 2.0
        midpoint_y = (first.y + second.y) / 2.0
        return math.dist((midpoint_x, midpoint_y), (center.x, center.y))
    if constraint.constraint_type == ConstraintType.MIDPOINT:
        midpoint = entities[constraint.entity_ids[0]]
        first = entities[constraint.entity_ids[1]]
        second = entities[constraint.entity_ids[2]]
        return math.dist((midpoint.x, midpoint.y), ((first.x + second.x) / 2.0, (first.y + second.y) / 2.0))
    if constraint.constraint_type == ConstraintType.OFFSET:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        return abs(_distance_point_to_line(second.start, first) - float(constraint.value or 0.0))
    if constraint.constraint_type == ConstraintType.LOCK:
        locked = constraint.metadata.get("locked_state")
        entity = entities[constraint.entity_ids[0]]
        if isinstance(entity, Point3D) and isinstance(locked, dict):
            return math.dist((entity.x, entity.y), (locked["x"], locked["y"]))
    return 0.0


def apply_geometric(constraint: Constraint, entities: dict[str, object], tolerance: ConstraintTolerance) -> float:
    """Apply a single geometric constraint and return its resulting residual."""
    if constraint.constraint_type == ConstraintType.COINCIDENT:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        _set_point(second, first.x, first.y, first.z)
    elif constraint.constraint_type == ConstraintType.HORIZONTAL:
        entity = entities[constraint.entity_ids[0]]
        if isinstance(entity, Line):
            average = (entity.start.y + entity.end.y) / 2.0
            _set_point(entity.start, entity.start.x, average)
            _set_point(entity.end, entity.end.x, average)
    elif constraint.constraint_type == ConstraintType.VERTICAL:
        entity = entities[constraint.entity_ids[0]]
        if isinstance(entity, Line):
            average = (entity.start.x + entity.end.x) / 2.0
            _set_point(entity.start, average, entity.start.y)
            _set_point(entity.end, average, entity.end.y)
    elif constraint.constraint_type == ConstraintType.PARALLEL:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        dx, dy = _normalize(*_line_direction(first))
        length = _line_length(second)
        _set_point(second.end, second.start.x + dx * length, second.start.y + dy * length)
    elif constraint.constraint_type == ConstraintType.PERPENDICULAR:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        dx, dy = _normalize(*_line_direction(first))
        length = _line_length(second)
        perp_x, perp_y = -dy, dx
        _set_point(second.end, second.start.x + perp_x * length, second.start.y + perp_y * length)
    elif constraint.constraint_type == ConstraintType.CONCENTRIC:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        _set_point(second.center, first.center.x, first.center.y, first.center.z)
    elif constraint.constraint_type == ConstraintType.TANGENT:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        if isinstance(first, Line) and isinstance(second, Circle):
            dx, dy = _line_direction(first)
            nx, ny = _normalize(-dy, dx)
            projection = _project_point_to_line(second.center, first)
            _set_point(second.center, projection[0] + nx * second.radius, projection[1] + ny * second.radius, second.center.z)
    elif constraint.constraint_type == ConstraintType.EQUAL_LENGTH:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        dx, dy = _normalize(*_line_direction(second))
        target = _line_length(first)
        _set_point(second.end, second.start.x + dx * target, second.start.y + dy * target)
    elif constraint.constraint_type == ConstraintType.EQUAL_RADIUS:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        second.radius = first.radius
    elif constraint.constraint_type == ConstraintType.SYMMETRY:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        center = entities[constraint.entity_ids[2]]
        _set_point(second, 2.0 * center.x - first.x, 2.0 * center.y - first.y, second.z)
    elif constraint.constraint_type == ConstraintType.MIDPOINT:
        midpoint = entities[constraint.entity_ids[0]]
        first = entities[constraint.entity_ids[1]]
        second = entities[constraint.entity_ids[2]]
        _set_point(midpoint, (first.x + second.x) / 2.0, (first.y + second.y) / 2.0, midpoint.z)
    elif constraint.constraint_type == ConstraintType.OFFSET:
        first = entities[constraint.entity_ids[0]]
        second = entities[constraint.entity_ids[1]]
        dx, dy = _line_direction(first)
        nx, ny = _normalize(-dy, dx)
        distance = float(constraint.value or 0.0)
        sx, sy = first.start.x + nx * distance, first.start.y + ny * distance
        ex, ey = first.end.x + nx * distance, first.end.y + ny * distance
        _set_point(second.start, sx, sy)
        _set_point(second.end, ex, ey)
    elif constraint.constraint_type == ConstraintType.LOCK:
        entity = entities[constraint.entity_ids[0]]
        locked = constraint.metadata.get("locked_state")
        if isinstance(entity, Point3D) and isinstance(locked, dict):
            _set_point(entity, locked["x"], locked["y"], locked.get("z", entity.z))
    return evaluate_geometric(constraint, entities, tolerance)


def _project_point_to_line(point: Point3D, line: Line) -> tuple[float, float]:
    dx = line.end.x - line.start.x
    dy = line.end.y - line.start.y
    length_sq = dx * dx + dy * dy
    if length_sq == 0.0:
        return (line.start.x, line.start.y)
    scale = ((point.x - line.start.x) * dx + (point.y - line.start.y) * dy) / length_sq
    return (line.start.x + scale * dx, line.start.y + scale * dy)


def _distance_point_to_line(point: Point3D, line: Line) -> float:
    px, py = _project_point_to_line(point, line)
    return math.dist((point.x, point.y), (px, py))
