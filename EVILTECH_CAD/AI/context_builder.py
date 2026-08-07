"""Context construction for the AI Engineering Assistant."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from IO.file_manager import ProjectSnapshot
from MODELING.part import PartModel


@dataclass(slots=True)
class AssistantContext:
    """Normalized engineering context attached to an assistant turn."""

    project_id: str | None
    project_name: str
    discipline: str
    feature_count: int
    entity_count: int
    material_key: str
    metadata: dict[str, Any] = field(default_factory=dict)


class ContextBuilder:
    """Build assistant context records from project and modeling state."""

    def build_for_part(
        self,
        part: PartModel,
        project_snapshot: ProjectSnapshot | None = None,
        discipline: str = "mechanical_engineering",
        material_key: str = "aluminum-6061",
    ) -> AssistantContext:
        """Build normalized assistant context for a part review."""
        body = part.primary_body()
        return AssistantContext(
            project_id=None if project_snapshot is None else project_snapshot.metadata.project_id,
            project_name=part.name,
            discipline=discipline,
            feature_count=part.feature_tree.feature_count(),
            entity_count=1,
            material_key=material_key,
            metadata={
                "body_volume": body.volume,
                "face_count": body.face_count,
                "project_path": None if project_snapshot is None else str(project_snapshot.project_path),
            },
        )