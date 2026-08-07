"""Generic configuration helpers for EvilTech CAD subsystems."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from UTILS.helpers import deep_merge


@dataclass(slots=True)
class ConfigSection:
    """A named configuration section."""

    name: str
    values: dict[str, Any] = field(default_factory=dict)


class ConfigManager:
    """Store and merge named configuration sections."""

    def __init__(self) -> None:
        self._sections: dict[str, ConfigSection] = {}

    def register(self, name: str, values: Mapping[str, Any]) -> ConfigSection:
        """Register or replace a named section."""
        section = ConfigSection(name=name, values=dict(values))
        self._sections[name] = section
        return section

    def merge(self, name: str, override: Mapping[str, Any]) -> ConfigSection:
        """Deep-merge values into an existing section."""
        existing = self._sections.get(name, ConfigSection(name=name))
        merged = ConfigSection(name=name, values=deep_merge(existing.values, override))
        self._sections[name] = merged
        return merged

    def get(self, name: str) -> ConfigSection:
        """Return a named section."""
        return self._sections[name]
