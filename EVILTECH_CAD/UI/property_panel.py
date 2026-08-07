"""Property and settings panels for the EvilTech CAD UI framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from UI.hierarchy_panel import DockPanel


@dataclass(slots=True)
class PropertiesPanel(DockPanel):
    """Properties panel for selected object attributes."""

    values: dict[str, Any] = field(default_factory=dict)

    def __init__(self, values: dict[str, Any]) -> None:
        DockPanel.__init__(self, title="Properties")
        self.values = dict(values)

    def get(self, key: str) -> Any:
        """Return a property value by key."""
        return self.values[key]


@dataclass(slots=True)
class SettingsWindow:
    """Settings window for UI preferences and configuration."""

    values: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str) -> Any:
        """Return a stored setting by key."""
        return self.values[key]

    def set(self, key: str, value: Any) -> None:
        """Store a setting value."""
        self.values[key] = value
