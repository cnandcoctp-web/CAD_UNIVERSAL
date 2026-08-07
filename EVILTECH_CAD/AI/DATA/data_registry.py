"""Registry of AI data loaders."""

from __future__ import annotations

from dataclasses import dataclass

from AI.DATA.assembly_loader import AssemblyLoader
from AI.DATA.geometry_loader import GeometryLoader
from AI.DATA.material_loader import MaterialLoader
from AI.DATA.project_loader import AIProjectLoader


@dataclass(slots=True)
class DataRegistry:
    """Bundle of AI data loaders."""

    materials: MaterialLoader = MaterialLoader()
    geometry: GeometryLoader = GeometryLoader()
    assemblies: AssemblyLoader = AssemblyLoader()
    projects: AIProjectLoader = AIProjectLoader()
