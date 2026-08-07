"""Shared body primitives for the modeling engine."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ModelBody:
    """A lightweight parametric body representation."""

    name: str
    volume: float
    face_count: int
    edge_count: int
    body_count: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)

    def clone(self, name: str | None = None) -> "ModelBody":
        """Return a copy of the body."""
        return ModelBody(
            name=name or self.name,
            volume=self.volume,
            face_count=self.face_count,
            edge_count=self.edge_count,
            body_count=self.body_count,
            metadata=deepcopy(self.metadata),
        )