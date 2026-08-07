"""Material-data loaders for the AI pipeline."""

from __future__ import annotations

from DATA.materials import MaterialSpecification, build_material_library


class MaterialLoader:
    """Load material specifications into the AI pipeline."""

    def load(self) -> dict[str, MaterialSpecification]:
        """Return the material catalog entries."""
        return dict(build_material_library().entries)
