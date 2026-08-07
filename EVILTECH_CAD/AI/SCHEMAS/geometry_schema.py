"""Geometry-related AI schema definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class GeometryEntitySnapshot:
    """Serializable geometry summary for a part or assembly component."""

    identifier: str
    entity_type: str
    volume: float = 0.0
    face_count: int = 0
    edge_count: int = 0
    feature_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GeometryDataset:
    """Geometry payload passed through the AI pipeline."""

    project_name: str
    entities: list[GeometryEntitySnapshot] = field(default_factory=list)
    material_key: str = "aluminum-6061"

    def total_volume(self) -> float:
        """Return the combined volume of all entities."""
        return sum(entity.volume for entity in self.entities)

    def total_faces(self) -> int:
        """Return the combined face count of all entities."""
        return sum(entity.face_count for entity in self.entities)
