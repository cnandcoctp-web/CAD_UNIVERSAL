"""Comprehensive regression tests for the EvilTech CAD mathematical engine."""

# pyright: reportMissingImports=false

from __future__ import annotations

import math

import pytest

from MATH_ENGINE.algebra import CoordinateSystem, Vector3
from MATH_ENGINE.interpolation import cubic_interpolate, linear_interpolate
from MATH_ENGINE.matrix import Matrix
from MATH_ENGINE.numerical import estimate_derivative, estimate_integral, solve_linear_system
from MATH_ENGINE.quaternion import Quaternion
from MATH_ENGINE.solver import NewtonRaphsonSolver
from MATH_ENGINE.tolerance import Tolerance, is_close
from MATH_ENGINE.transforms import Transform
from MATH_ENGINE.utilities import clamp, ensure_finite, normalize_angle, safe_divide


def test_vector3_operations() -> None:
    left = Vector3(1.0, -2.0, 3.0)
    right = Vector3(4.0, 5.0, -6.0)

    assert left + right == pytest.approx(Vector3(5.0, 3.0, -3.0))
    assert left - right == pytest.approx(Vector3(-3.0, -7.0, 9.0))
    assert left.dot(right) == pytest.approx(-24.0)
    assert left.cross(right) == pytest.approx(Vector3(-3.0, 18.0, 13.0))
    assert left.magnitude() == pytest.approx(math.sqrt(14.0))
    assert left.normalized() == pytest.approx(Vector3(1.0 / math.sqrt(14.0), -2.0 / math.sqrt(14.0), 3.0 / math.sqrt(14.0)))


def test_vector3_distance_and_projection() -> None:
    base = Vector3(1.0, 2.0, 3.0)
    target = Vector3(4.0, 6.0, 3.0)

    assert base.distance_to(target) == pytest.approx(5.0)
    projection = Vector3(2.0, 0.0, 0.0).project_onto(Vector3(1.0, 0.0, 0.0))
    assert projection == pytest.approx(Vector3(2.0, 0.0, 0.0))


def test_coordinate_system_round_trip() -> None:
    frame = CoordinateSystem(origin=Vector3(1.0, 2.0, 3.0), basis_x=Vector3(1.0, 0.0, 0.0), basis_y=Vector3(0.0, 1.0, 0.0), basis_z=Vector3(0.0, 0.0, 1.0))

    local = frame.to_local(Vector3(4.0, 5.0, 6.0))
    assert local == pytest.approx(Vector3(3.0, 3.0, 3.0))
    assert frame.to_global(local) == pytest.approx(Vector3(4.0, 5.0, 6.0))


def test_matrix_basic_operations() -> None:
    matrix = Matrix([[1.0, 2.0], [3.0, 4.0]])
    other = Matrix([[5.0, 6.0], [7.0, 8.0]])

    assert matrix + other == pytest.approx(Matrix([[6.0, 8.0], [10.0, 12.0]]))
    assert matrix * other == pytest.approx(Matrix([[19.0, 22.0], [43.0, 50.0]]))
    assert matrix.determinant() == pytest.approx(-2.0)
    inverse = matrix.inverse()
    assert inverse.data[0][0] == pytest.approx(-2.0, rel=1e-6)
    assert inverse.data[0][1] == pytest.approx(1.0, rel=1e-6)
    assert inverse.data[1][0] == pytest.approx(1.5, rel=1e-6)
    assert inverse.data[1][1] == pytest.approx(-0.5, rel=1e-6)


def test_matrix_vector_multiplication() -> None:
    matrix = Matrix([[1.0, 0.0, 2.0], [0.0, 1.0, 3.0], [0.0, 0.0, 1.0]])
    vector = Vector3(1.0, 2.0, 3.0)

    result = matrix * vector
    assert result == pytest.approx(Vector3(7.0, 11.0, 3.0))


def test_quaternion_operations() -> None:
    quaternion = Quaternion(1.0, 0.0, 0.0, 0.0)
    assert quaternion.norm() == pytest.approx(1.0)
    assert quaternion.normalized() == quaternion

    rotation = Quaternion.from_axis_angle(Vector3(0.0, 0.0, 1.0), math.pi / 2.0)
    rotated = rotation.rotate_vector(Vector3(1.0, 0.0, 0.0))
    assert rotated == pytest.approx(Vector3(0.0, 1.0, 0.0))


def test_quaternion_multiplication() -> None:
    first = Quaternion.from_axis_angle(Vector3(0.0, 0.0, 1.0), math.pi / 2.0)
    second = Quaternion.from_axis_angle(Vector3(0.0, 0.0, 1.0), math.pi / 2.0)
    combined = first * second
    rotated = combined.rotate_vector(Vector3(1.0, 0.0, 0.0))
    assert rotated == pytest.approx(Vector3(-1.0, 0.0, 0.0))


def test_transform_translation_rotation_and_scale() -> None:
    translation = Transform.translation(1.0, 2.0, 3.0)
    rotated = Transform.rotation_z(math.pi / 2.0)
    scaled = Transform.scale(2.0, 2.0, 2.0)

    composed = translation * rotated * scaled
    point = composed.transform_point(Vector3(1.0, 0.0, 0.0))
    assert point == pytest.approx(Vector3(-4.0, 4.0, 6.0))


def test_transform_vector_transformation() -> None:
    transform = Transform.rotation_z(math.pi / 2.0)
    vector = transform.transform_vector(Vector3(1.0, 0.0, 0.0))
    assert vector == pytest.approx(Vector3(0.0, 1.0, 0.0))


def test_numerical_linear_system() -> None:
    matrix = Matrix([[2.0, 1.0], [1.0, 3.0]])
    vector = [1.0, 2.0]

    solution = solve_linear_system(matrix, vector)
    assert solution == pytest.approx([0.2, 0.6])


def test_numerical_derivative_and_integral() -> None:
    def linear(x: float) -> float:
        return 2.0 * x + 1.0

    assert estimate_derivative(linear, 2.0, h=1e-4) == pytest.approx(2.0, rel=1e-4)
    assert estimate_integral(linear, 0.0, 4.0, steps=200) == pytest.approx(20.0, rel=1e-3)


def test_newton_raphson_solver() -> None:
    solver = NewtonRaphsonSolver()

    def function(x: float) -> float:
        return x * x - 4.0

    result = solver.solve(function, 1.5)
    assert result == pytest.approx(2.0, rel=1e-6)


def test_tolerance_and_is_close() -> None:
    tolerance = Tolerance(absolute=1e-6, relative=1e-6)
    assert tolerance.is_close(1.0, 1.0 + 5e-7)
    assert not tolerance.is_close(1.0, 2.0)
    assert is_close(1.0, 1.0 + 5e-7)


def test_interpolation_helpers() -> None:
    assert linear_interpolate(0.0, 10.0, 0.5) == pytest.approx(5.0)
    assert cubic_interpolate(0.0, 1.0, 2.0, 3.0, 0.5) == pytest.approx(1.5)


def test_utilities_helpers() -> None:
    assert clamp(5.0, 0.0, 3.0) == pytest.approx(3.0)
    assert normalize_angle(math.pi + 0.5) == pytest.approx(math.pi + 0.5)
    assert safe_divide(4.0, 2.0) == pytest.approx(2.0)
    assert safe_divide(4.0, 0.0) == pytest.approx(0.0)
    assert ensure_finite(1.0 / 2.0) == pytest.approx(0.5)
