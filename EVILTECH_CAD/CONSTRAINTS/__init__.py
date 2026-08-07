"""Geometric constraint engine package for EvilTech CAD."""

from CONSTRAINTS.constraint_registry import Constraint, ConstraintEvent, ConstraintRegistry, ConstraintType
from CONSTRAINTS.constraint_solver import (
    ConstraintDependencyGraph,
    ConstraintHistory,
    ConstraintManager,
    ConstraintPersistence,
    ConstraintSolver,
    SolveResult,
)
from CONSTRAINTS.tolerance_constraints import ConstraintTolerance, ConstraintValidationResult, ConstraintValidator

__all__ = [
    "Constraint",
    "ConstraintDependencyGraph",
    "ConstraintEvent",
    "ConstraintHistory",
    "ConstraintManager",
    "ConstraintPersistence",
    "ConstraintRegistry",
    "ConstraintSolver",
    "ConstraintTolerance",
    "ConstraintType",
    "ConstraintValidationResult",
    "ConstraintValidator",
    "SolveResult",
]