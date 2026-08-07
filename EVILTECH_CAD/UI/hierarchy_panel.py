"""Docking and hierarchical panel primitives for the EvilTech CAD UI framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DockPanel:
    """Base class for dockable panels."""

    title: str

    def __post_init__(self) -> None:
        if not self.title:
            raise ValueError("title must be non-empty")


@dataclass(slots=True)
class ProjectExplorer(DockPanel):
    """Project explorer panel."""

    projects: list[str] = field(default_factory=list)

    def __init__(self, projects: list[str]) -> None:
        DockPanel.__init__(self, title="Project Explorer")
        self.projects = list(projects)


@dataclass(slots=True)
class ObjectTree(DockPanel):
    """Object tree panel."""

    nodes: list[str] = field(default_factory=list)

    def __init__(self, nodes: list[str]) -> None:
        DockPanel.__init__(self, title="Object Tree")
        self.nodes = list(nodes)


@dataclass(slots=True)
class InspectorPanel(DockPanel):
    """Inspector panel for selections and diagnostics."""

    details: dict[str, Any] = field(default_factory=dict)

    def __init__(self, details: dict[str, Any]) -> None:
        DockPanel.__init__(self, title="Inspector")
        self.details = dict(details)


@dataclass(slots=True)
class LayerManager(DockPanel):
    """Layer manager panel."""

    layers: list[str] = field(default_factory=list)

    def __init__(self, layers: list[str]) -> None:
        DockPanel.__init__(self, title="Layer Manager")
        self.layers = list(layers)

    def layer_count(self) -> int:
        """Return the number of tracked layers."""
        return len(self.layers)


@dataclass(slots=True)
class MaterialBrowser(DockPanel):
    """Material browser panel."""

    materials: list[str] = field(default_factory=list)

    def __init__(self, materials: list[str]) -> None:
        DockPanel.__init__(self, title="Material Browser")
        self.materials = list(materials)

    def item_count(self) -> int:
        """Return the number of listed materials."""
        return len(self.materials)


@dataclass(slots=True)
class AssetBrowser(DockPanel):
    """Asset browser panel."""

    assets: list[str] = field(default_factory=list)

    def __init__(self, assets: list[str]) -> None:
        DockPanel.__init__(self, title="Asset Browser")
        self.assets = list(assets)

    def item_count(self) -> int:
        """Return the number of listed assets."""
        return len(self.assets)


class DockingFramework:
    """Track docked panels by workspace zone."""

    def __init__(self) -> None:
        self._zones: dict[str, list[DockPanel]] = {"left": [], "right": [], "top": [], "bottom": [], "center": []}

    def dock(self, panel: DockPanel, zone: str) -> None:
        """Dock a panel into a named zone."""
        if not isinstance(panel, DockPanel):
            raise TypeError("panel must be a DockPanel")
        if zone not in self._zones:
            raise ValueError(f"Unsupported docking zone '{zone}'")
        self._zones[zone].append(panel)

    def panel_count(self, zone: str) -> int:
        """Return the number of panels in a docking zone."""
        if zone not in self._zones:
            raise ValueError(f"Unsupported docking zone '{zone}'")
        return len(self._zones[zone])

    def snapshot(self) -> dict[str, list[str]]:
        """Return a serializable layout snapshot."""
        return {zone: [panel.title for panel in panels] for zone, panels in self._zones.items()}


class WorkspaceLayoutManager:
    """Save and recall named workspace layouts."""

    def __init__(self, docking: DockingFramework) -> None:
        if not isinstance(docking, DockingFramework):
            raise TypeError("docking must be a DockingFramework")
        self.docking = docking
        self._layouts: dict[str, dict[str, list[str]]] = {}

    def save_layout(self, name: str) -> None:
        """Save the current docking layout by name."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        self._layouts[name] = self.docking.snapshot()

    def available_layouts(self) -> list[str]:
        """Return saved layout names."""
        return list(self._layouts.keys())
