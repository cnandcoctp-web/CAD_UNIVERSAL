"""Geometry-data loaders for the AI pipeline."""

from __future__ import annotations

from MODELING.part import PartModel

from AI.SCHEMAS.geometry_schema import GeometryDataset, GeometryEntitySnapshot


class GeometryLoader:
    """Convert part models into AI geometry datasets."""

    def load_part(self, part: PartModel, material_key: str = "aluminum-6061") -> GeometryDataset:
        """Create a geometry dataset from a part model."""
        body = part.primary_body()
        entity = GeometryEntitySnapshot(
            identifier=part.name,
            entity_type="part",
            volume=body.volume,
            face_count=body.face_count,
            edge_count=body.edge_count,
            feature_count=part.feature_tree.feature_count(),
        )
        return GeometryDataset(project_name=part.name, entities=[entity], material_key=material_key)
