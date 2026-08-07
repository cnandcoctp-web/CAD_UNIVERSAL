"""Viewport UI primitives for the EvilTech CAD UI framework."""

from __future__ import annotations

from dataclasses import dataclass, field

from RENDERING.camera import BaseCamera, CameraController
from RENDERING.renderer import Renderer


@dataclass(slots=True)
class UIViewport:
    """A UI-facing viewport bound to a renderer and camera."""

    identifier: str
    title: str
    renderer: Renderer
    camera: BaseCamera
    controller: CameraController = field(init=False)

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError("identifier must be non-empty")
        if not self.title:
            raise ValueError("title must be non-empty")
        if not isinstance(self.renderer, Renderer):
            raise TypeError("renderer must be a Renderer")
        if not isinstance(self.camera, BaseCamera):
            raise TypeError("camera must be a BaseCamera")
        self.controller = CameraController(self.camera)

    def render_frame(self) -> dict[str, object]:
        """Render the active frame for this viewport."""
        return self.renderer.render(self.camera)


class UIViewportManager:
    """Manage UI viewports and the active viewport selection."""

    def __init__(self, viewports: list[UIViewport] | None = None) -> None:
        self._viewports: dict[str, UIViewport] = {}
        self._active_identifier: str | None = None
        for viewport in viewports or []:
            self.register(viewport)

    def register(self, viewport: UIViewport) -> None:
        """Register a UI viewport."""
        if not isinstance(viewport, UIViewport):
            raise TypeError("viewport must be a UIViewport")
        self._viewports[viewport.identifier] = viewport
        if self._active_identifier is None:
            self._active_identifier = viewport.identifier

    def active_viewport(self) -> UIViewport:
        """Return the active viewport."""
        if self._active_identifier is None:
            raise ValueError("No active viewport is registered")
        return self._viewports[self._active_identifier]

    def activate(self, identifier: str) -> None:
        """Activate a viewport by identifier."""
        if identifier not in self._viewports:
            raise KeyError(f"Viewport '{identifier}' was not found")
        self._active_identifier = identifier
