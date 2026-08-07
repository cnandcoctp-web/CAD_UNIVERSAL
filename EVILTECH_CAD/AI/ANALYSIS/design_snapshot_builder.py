"""Design-snapshot builder for the AI pipeline."""

from __future__ import annotations

from CONSTRAINTS.constraint_solver import ConstraintManager
from MODELING.assembly import Assembly
from MODELING.part import PartModel

from AI.SCHEMAS.analysis_schema import DesignSnapshot
from AI.SCHEMAS.geometry_schema import GeometryDataset


class DesignSnapshotBuilder:
    """Build normalized design snapshots from modeling state."""

    def build_part_snapshot(self, part: PartModel, geometry: GeometryDataset, constraints: ConstraintManager | None = None) -> DesignSnapshot:
        """Build a snapshot for a part model."""
        constraint_summary = {"constraint_count": len(constraints.constraints)} if constraints is not None else {"constraint_count": 0}
        return DesignSnapshot(
            project_name=part.name,
            geometry=geometry,
            feature_names=part.feature_tree.feature_names(),
            materials=[geometry.material_key],
            constraint_summary=constraint_summary,
            metadata={"history_entries": len(part.design_history.entries())},
        )

    def build_assembly_snapshot(self, assembly: Assembly, geometry: GeometryDataset) -> DesignSnapshot:
        """Build a snapshot for an assembly."""
        return DesignSnapshot(
            project_name=assembly.name,
            geometry=geometry,
            feature_names=[],
            materials=[geometry.material_key],
            assembly_summary={"components": assembly.component_count(), "mates": len(assembly.mates)},
        )
