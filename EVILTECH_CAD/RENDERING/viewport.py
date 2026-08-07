"""Viewport primitives and managers for rendering."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Viewport:
    """A render viewport describing a drawable rectangular region."""

    identifier: str
    width: int
    height: int
    x: int = 0
    y: int = 0

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError("identifier must be non-empty")
        if self.width <= 0 or self.height <= 0:
            raise ValueError("width and height must be positive")

    def resize(self, width: int, height: int) -> None:
        """Resize the viewport dimensions."""
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        self.width = width
        self.height = height

    def contains(self, x: int, y: int) -> bool:
        """Determine whether a screen-space coordinate lies inside the viewport."""
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height


class ViewportManager:
    """Manage multiple viewports for 2D and 3D workspaces."""

    def __init__(self, viewports: list[Viewport] | None = None) -> None:
        self._viewports: dict[str, Viewport] = {}
        for viewport in viewports or []:
            self.register(viewport)

    def register(self, viewport: Viewport) -> None:
        """Register a viewport."""
        if not isinstance(viewport, Viewport):
            raise TypeError("viewport must be a Viewport")
        self._viewports[viewport.identifier] = viewport

    def get(self, identifier: str) -> Viewport:
        """Return a viewport by identifier."""
        if identifier not in self._viewports:
            raise KeyError(f"Viewport '{identifier}' was not found")
        return self._viewports[identifier]

    def all(self) -> list[Viewport]:
        """Return all registered viewports."""
        return list(self._viewports.values())
