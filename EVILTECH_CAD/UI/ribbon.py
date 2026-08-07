"""Ribbon toolbar primitives for the EvilTech CAD UI framework."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RibbonTab:
    """A ribbon tab grouping related commands."""

    name: str
    commands: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must be non-empty")


class RibbonToolbar:
    """A headless ribbon toolbar model."""

    def __init__(self, tabs: list[RibbonTab] | None = None) -> None:
        self._tabs: dict[str, RibbonTab] = {}
        for tab in tabs or []:
            self.add_tab(tab)

    def add_tab(self, tab: RibbonTab) -> None:
        """Register a ribbon tab."""
        if not isinstance(tab, RibbonTab):
            raise TypeError("tab must be a RibbonTab")
        self._tabs[tab.name] = tab

    def tab_names(self) -> list[str]:
        """Return the registered ribbon tab names."""
        return list(self._tabs.keys())
