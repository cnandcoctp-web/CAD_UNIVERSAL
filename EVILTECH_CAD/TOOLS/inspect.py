"""Inspection tools for EvilTech CAD."""

from __future__ import annotations

from MODELING.assembly import Assembly
from MODELING.feature import ModelBody
from MODELING.part import PartModel


class InspectionService:
    """Generate inspection summaries for modeling objects."""

    def inspect_part(self, part: PartModel) -> dict[str, object]:
        """Return a summary of a part model."""
        body = part.primary_body()
        return {
            "name": part.name,
            "feature_count": part.feature_tree.feature_count(),
            "volume": body.volume,
            "faces": body.face_count,
        }

    def inspect_body(self, body: ModelBody) -> dict[str, object]:
        """Return a summary of a lightweight model body."""
        return {"name": body.name, "volume": body.volume, "faces": body.face_count, "edges": body.edge_count}

    def inspect_assembly(self, assembly: Assembly) -> dict[str, object]:
        """Return a summary of an assembly."""
        return {"name": assembly.name, "components": assembly.component_count(), "mates": len(assembly.mates)}
