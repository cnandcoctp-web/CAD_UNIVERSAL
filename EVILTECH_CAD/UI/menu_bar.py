"""Menu bar primitives for the EvilTech CAD UI framework."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(slots=True)
class MenuItem:
    """A menu item bound to a callable action."""

    name: str
    action: Callable[[], None]

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must be non-empty")
        if not callable(self.action):
            raise TypeError("action must be callable")


class MenuBar:
    """A simple menu bar containing named menu items."""

    def __init__(self, items: list[MenuItem] | None = None) -> None:
        self._items: dict[str, MenuItem] = {}
        for item in items or []:
            self.add_item(item)

    def add_item(self, item: MenuItem) -> None:
        """Add a menu item to the bar."""
        if not isinstance(item, MenuItem):
            raise TypeError("item must be a MenuItem")
        self._items[item.name] = item

    def trigger(self, name: str) -> None:
        """Invoke a menu item by name."""
        if name not in self._items:
            raise KeyError(f"Menu item '{name}' was not found")
        self._items[name].action()

    def names(self) -> list[str]:
        """Return the registered menu names."""
        return list(self._items.keys())
