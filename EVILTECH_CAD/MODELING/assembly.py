"""Assembly managers and component structures for the modeling engine."""

from __future__ import annotations

from dataclasses import dataclass, field

from MODELING.part import PartModel


class PartManager:
    """Manage reusable part definitions."""

    def __init__(self) -> None:
        self._parts: dict[str, PartModel] = {}

    def register(self, part: PartModel) -> None:
        """Register a part model by name."""
        if not isinstance(part, PartModel):
            raise TypeError("part must be a PartModel")
        self._parts[part.name] = part


class ComponentManager:
    """Manage instantiated assembly components."""

    def __init__(self) -> None:
        self._components: dict[str, PartModel] = {}

    def add_component(self, component_id: str, part: PartModel) -> None:
        """Add a component instance."""
        self._components[component_id] = part

    def get_component(self, component_id: str) -> PartModel:
        """Return a component by identifier."""
        return self._components[component_id]


@dataclass(slots=True)
class Mate:
    """Assembly mate descriptor."""

    name: str
    first_component: str
    second_component: str
    mate_type: str


@dataclass(slots=True)
class AssemblyTree:
    """Assembly tree container."""

    nodes: list[str] = field(default_factory=list)

    def node_names(self) -> list[str]:
        """Return assembly node names."""
        return list(self.nodes)


@dataclass(slots=True)
class ExplodedView:
    """Exploded-view descriptor."""

    name: str
    offsets: dict[str, tuple[float, float, float]] = field(default_factory=dict)


@dataclass(slots=True)
class Assembly:
    """Assembly model containing components and mates."""

    name: str
    components: list[str] = field(default_factory=list)
    mates: list[Mate] = field(default_factory=list)
    assembly_tree: AssemblyTree = field(default_factory=AssemblyTree)

    def component_count(self) -> int:
        """Return the number of components in the assembly."""
        return len(self.components)


class AssemblyManager:
    """Create and manage assemblies."""

    def __init__(self, component_manager: ComponentManager) -> None:
        self.component_manager = component_manager
        self._assemblies: dict[str, Assembly] = {}
        self._exploded_views: dict[str, ExplodedView] = {}

    def create_assembly(self, name: str) -> Assembly:
        """Create a named assembly."""
        assembly = Assembly(name=name)
        self._assemblies[name] = assembly
        return assembly

    def add_to_assembly(self, assembly_name: str, component_id: str) -> None:
        """Add a component to an assembly."""
        assembly = self._assemblies[assembly_name]
        self.component_manager.get_component(component_id)
        assembly.components.append(component_id)
        assembly.assembly_tree.nodes.append(component_id)

    def add_mate(self, assembly_name: str, mate: Mate) -> None:
        """Attach a mate to an assembly."""
        self._assemblies[assembly_name].mates.append(mate)

    def create_exploded_view(self, assembly_name: str, offsets: dict[str, tuple[float, float, float]]) -> ExplodedView:
        """Create an exploded view for an assembly."""
        exploded = ExplodedView(name=f"{assembly_name}-exploded", offsets=dict(offsets))
        self._exploded_views[assembly_name] = exploded
        return exploded
