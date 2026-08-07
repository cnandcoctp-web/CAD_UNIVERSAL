"""Constraint type registry and core constraint models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class ConstraintType(str, Enum):
    """Supported geometric and dimensional constraint types."""

    COINCIDENT = "coincident"
    PARALLEL = "parallel"
    PERPENDICULAR = "perpendicular"
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    DISTANCE = "distance"
    ANGLE = "angle"
    RADIUS = "radius"
    DIAMETER = "diameter"
    CONCENTRIC = "concentric"
    TANGENT = "tangent"
    EQUAL_LENGTH = "equal_length"
    EQUAL_RADIUS = "equal_radius"
    SYMMETRY = "symmetry"
    MIDPOINT = "midpoint"
    OFFSET = "offset"
    LOCK = "lock"
    REFERENCE = "reference"
    DRIVING = "driving"
    DRIVEN = "driven"


@dataclass(slots=True)
class Constraint:
    """A serializable constraint record bound to named geometry entities."""

    constraint_id: str
    constraint_type: ConstraintType
    entity_ids: tuple[str, ...]
    value: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    active: bool = True
    dependencies: tuple[str, ...] = field(default_factory=tuple)
    mode: str = "driving"

    def __post_init__(self) -> None:
        if not self.constraint_id:
            raise ValueError("constraint_id must be non-empty")
        if not isinstance(self.constraint_type, ConstraintType):
            raise TypeError("constraint_type must be a ConstraintType")
        if not self.entity_ids:
            raise ValueError("entity_ids must be non-empty")
        if self.mode not in {"driving", "driven", "reference"}:
            raise ValueError("mode must be 'driving', 'driven', or 'reference'")

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable representation of the constraint."""
        return {
            "constraint_id": self.constraint_id,
            "constraint_type": self.constraint_type.value,
            "entity_ids": list(self.entity_ids),
            "value": self.value,
            "metadata": dict(self.metadata),
            "active": self.active,
            "dependencies": list(self.dependencies),
            "mode": self.mode,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Constraint":
        """Create a constraint from a persisted dictionary."""
        return cls(
            constraint_id=str(payload["constraint_id"]),
            constraint_type=ConstraintType(str(payload["constraint_type"])),
            entity_ids=tuple(str(item) for item in payload["entity_ids"]),
            value=payload.get("value"),
            metadata=dict(payload.get("metadata", {})),
            active=bool(payload.get("active", True)),
            dependencies=tuple(str(item) for item in payload.get("dependencies", [])),
            mode=str(payload.get("mode", "driving")),
        )


@dataclass(slots=True)
class ConstraintEvent:
    """A lightweight event record for constraint-engine activity."""

    event_type: str
    detail: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ConstraintRegistry:
    """Register supported constraint types and create constraint instances."""

    def __init__(self) -> None:
        self._definitions: dict[ConstraintType, dict[str, Any]] = {}
        self._register_builtins()

    def _register_builtins(self) -> None:
        for constraint_type in ConstraintType:
            self.register(
                constraint_type,
                {
                    "name": constraint_type.value,
                    "category": "dimensional" if constraint_type in {ConstraintType.DISTANCE, ConstraintType.ANGLE, ConstraintType.RADIUS, ConstraintType.DIAMETER, ConstraintType.OFFSET} else "geometric",
                },
            )

    def register(self, constraint_type: ConstraintType, definition: dict[str, Any]) -> None:
        """Register a constraint definition."""
        if not isinstance(constraint_type, ConstraintType):
            raise TypeError("constraint_type must be a ConstraintType")
        self._definitions[constraint_type] = dict(definition)

    def supported_types(self) -> list[ConstraintType]:
        """Return the registered constraint types."""
        return list(self._definitions.keys())

    def create_constraint(
        self,
        constraint_type: ConstraintType | str,
        entity_ids: tuple[str, ...],
        value: float | None = None,
        metadata: dict[str, Any] | None = None,
        dependencies: tuple[str, ...] | None = None,
        mode: str = "driving",
    ) -> Constraint:
        """Create a new constraint with a generated identifier."""
        resolved = ConstraintType(constraint_type) if isinstance(constraint_type, str) else constraint_type
        if resolved not in self._definitions:
            raise ValueError(f"Unsupported constraint type '{resolved}'")
        return Constraint(
            constraint_id=str(uuid4()),
            constraint_type=resolved,
            entity_ids=tuple(entity_ids),
            value=value,
            metadata=dict(metadata or {}),
            dependencies=tuple(dependencies or ()),
            mode=mode,
        )
