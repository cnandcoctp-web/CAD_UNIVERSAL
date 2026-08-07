"""Tolerance and validation helpers for the constraint engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from CONSTRAINTS.constraint_registry import Constraint, ConstraintType
from GEOMETRY.circle import Circle
from GEOMETRY.line import Line


@dataclass(slots=True)
class ConstraintTolerance:
    """Numeric tolerances used by constraint validation and solving."""

    linear: float = 1e-6
    angular: float = 1e-4


@dataclass(slots=True)
class ConstraintValidationResult:
    """Validation result for a set of constraints."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class ConstraintValidator:
    """Validate constraint definitions and detect common conflicts."""

    def __init__(self, tolerance: ConstraintTolerance | None = None) -> None:
        self.tolerance = tolerance or ConstraintTolerance()

    def validate_constraint(self, constraint: Constraint, entities: dict[str, object]) -> ConstraintValidationResult:
        """Validate a single constraint against available entities."""
        errors: list[str] = []
        if not isinstance(constraint, Constraint):
            return ConstraintValidationResult(is_valid=False, errors=["Constraint object is invalid"])
        for entity_id in constraint.entity_ids:
            if entity_id not in entities:
                errors.append(f"Missing entity '{entity_id}'")
        if constraint.constraint_type in {ConstraintType.DISTANCE, ConstraintType.RADIUS, ConstraintType.DIAMETER, ConstraintType.OFFSET}:
            if constraint.value is None or constraint.value < 0.0:
                errors.append(f"Constraint '{constraint.constraint_id}' requires a non-negative value")
        if constraint.constraint_type == ConstraintType.ANGLE:
            if constraint.value is None:
                errors.append(f"Constraint '{constraint.constraint_id}' requires an angle value")
        return ConstraintValidationResult(is_valid=not errors, errors=errors)

    def detect_conflicts(self, constraints: list[Constraint], entities: dict[str, object]) -> list[str]:
        """Detect conflicting or incompatible constraints."""
        conflicts: list[str] = []
        dimensional_keys: dict[tuple[ConstraintType, tuple[str, ...]], float] = {}
        horizontal_targets: set[tuple[str, ...]] = set()
        vertical_targets: set[tuple[str, ...]] = set()
        for constraint in constraints:
            if not constraint.active:
                continue
            validation = self.validate_constraint(constraint, entities)
            conflicts.extend(validation.errors)
            normalized_entities = tuple(sorted(constraint.entity_ids))
            key = (constraint.constraint_type, normalized_entities)
            if constraint.constraint_type in {ConstraintType.DISTANCE, ConstraintType.ANGLE, ConstraintType.RADIUS, ConstraintType.DIAMETER, ConstraintType.OFFSET} and constraint.value is not None:
                if key in dimensional_keys and abs(dimensional_keys[key] - constraint.value) > self.tolerance.linear:
                    conflicts.append(f"Conflicting values for {constraint.constraint_type.value} on {normalized_entities}")
                dimensional_keys[key] = float(constraint.value)
            if constraint.constraint_type == ConstraintType.HORIZONTAL:
                horizontal_targets.add(normalized_entities)
            if constraint.constraint_type == ConstraintType.VERTICAL:
                vertical_targets.add(normalized_entities)
        for target in horizontal_targets.intersection(vertical_targets):
            if len(target) == 1 and isinstance(entities.get(target[0]), Line):
                line = entities[target[0]]
                if line.length() > self.tolerance.linear:
                    conflicts.append(f"Line '{target[0]}' cannot be both horizontal and vertical")
            elif len(target) == 2:
                conflicts.append(f"Entity pair {target} cannot be both horizontal and vertical")
        return conflicts
