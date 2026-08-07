"""Toolbar primitives for the EvilTech CAD UI framework."""

from __future__ import annotations

from typing import Callable

from UI.viewport import UIViewportManager


class QuickAccessToolbar:
    """A quick-access toolbar for global actions."""

    def __init__(self, actions: dict[str, Callable[[], None]] | None = None) -> None:
        self._actions = dict(actions or {})
        for action in self._actions.values():
            if not callable(action):
                raise TypeError("toolbar actions must be callable")

    def invoke(self, name: str) -> None:
        """Invoke a registered quick-access action."""
        if name not in self._actions:
            raise KeyError(f"Action '{name}' was not found")
        self._actions[name]()


class ViewportControls:
    """High-level viewport controls for active camera interaction."""

    def __init__(self, viewport_manager: UIViewportManager) -> None:
        if not isinstance(viewport_manager, UIViewportManager):
            raise TypeError("viewport_manager must be a UIViewportManager")
        self.viewport_manager = viewport_manager

    def zoom_active(self, delta: float) -> None:
        """Zoom the active viewport camera."""
        self.viewport_manager.active_viewport().controller.zoom(delta)

    def pan_active(self, delta_x: float, delta_y: float) -> None:
        """Pan the active viewport camera."""
        self.viewport_manager.active_viewport().controller.pan(delta_x, delta_y)

    def orbit_active(self, yaw_degrees: float, pitch_degrees: float) -> None:
        """Orbit the active viewport camera."""
        self.viewport_manager.active_viewport().controller.orbit(yaw_degrees, pitch_degrees)
