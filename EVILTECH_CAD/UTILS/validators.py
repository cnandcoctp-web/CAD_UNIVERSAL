"""Validation helpers used across EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class ValidationReport:
    """Collect validation issues for a payload or workflow."""

    is_valid: bool = True
    errors: list[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add a validation error and mark the report invalid."""
        self.is_valid = False
        self.errors.append(message)


def require_non_empty_string(value: Any, field_name: str) -> str:
    """Validate a non-empty string field."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def require_numeric(value: Any, field_name: str) -> float:
    """Validate a finite numeric field."""
    if not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} must be numeric")
    return float(value)


def require_positive(value: Any, field_name: str, allow_zero: bool = False) -> float:
    """Validate a positive numeric field."""
    numeric = require_numeric(value, field_name)
    if allow_zero and numeric < 0.0:
        raise ValueError(f"{field_name} must be zero or positive")
    if not allow_zero and numeric <= 0.0:
        raise ValueError(f"{field_name} must be positive")
    return numeric


def require_type(value: Any, expected_type: type[T], field_name: str) -> T:
    """Validate that a value matches an expected type."""
    if not isinstance(value, expected_type):
        raise TypeError(f"{field_name} must be of type {expected_type.__name__}")
    return value
