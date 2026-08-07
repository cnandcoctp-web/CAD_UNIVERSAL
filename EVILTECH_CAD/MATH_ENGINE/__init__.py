"""Mathematical engine package for EvilTech CAD."""

from MATH_ENGINE.algebra import CoordinateSystem, Vector3
from MATH_ENGINE.interpolation import cubic_interpolate, linear_interpolate
from MATH_ENGINE.matrix import Matrix
from MATH_ENGINE.numerical import estimate_derivative, estimate_integral, solve_linear_system
from MATH_ENGINE.quaternion import Quaternion
from MATH_ENGINE.solver import NewtonRaphsonSolver
from MATH_ENGINE.tolerance import Tolerance, is_close
from MATH_ENGINE.transforms import Transform
from MATH_ENGINE.utilities import clamp, ensure_finite, normalize_angle, safe_divide

__all__ = [
    "CoordinateSystem",
    "Vector3",
    "Matrix",
    "Quaternion",
    "Transform",
    "Tolerance",
    "is_close",
    "linear_interpolate",
    "cubic_interpolate",
    "solve_linear_system",
    "estimate_derivative",
    "estimate_integral",
    "NewtonRaphsonSolver",
    "clamp",
    "ensure_finite",
    "normalize_angle",
    "safe_divide",
]
