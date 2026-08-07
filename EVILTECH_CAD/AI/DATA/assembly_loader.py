"""Assembly-data loaders for the AI pipeline."""

from __future__ import annotations

from MODELING.assembly import Assembly, ComponentManager

from AI.SCHEMAS.geometry_schema import GeometryDataset, GeometryEntitySnapshot


class AssemblyLoader:
    """Convert assemblies into AI geometry datasets."""

    def load_assembly(self, assembly: Assembly, components: ComponentManager, material_key: str = "steel-1018") -> GeometryDataset:
        """Create a geometry dataset from an assembly."""
        entities: list[GeometryEntitySnapshot] = []
        for component_id in assembly.components:
            part = components.get_component(component_id)
            body = part.primary_body()
            entities.append(
                GeometryEntitySnapshot(
                    identifier=component_id,
                    entity_type="component",
                    volume=body.volume,
                    face_count=body.face_count,
                    edge_count=body.edge_count,
                    feature_count=part.feature_tree.feature_count(),
                )
            )
        return GeometryDataset(project_name=assembly.name, entities=entities, material_key=material_key)
