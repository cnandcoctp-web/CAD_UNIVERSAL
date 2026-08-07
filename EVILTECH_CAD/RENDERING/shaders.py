"""Shader management for rendering."""

from __future__ import annotations


class ShaderManager:
    """Manage lightweight shader descriptors for the rendering engine."""

    def __init__(self) -> None:
        self._shaders: dict[str, object] = {}

    def register_shader(self, name: str, payload: object) -> None:
        """Register a shader payload by name."""
        if not name:
            raise ValueError("name must be non-empty")
        self._shaders[name] = payload

    def get_shader(self, name: str) -> object:
        """Return a shader payload by name."""
        if name not in self._shaders:
            raise KeyError(f"Shader '{name}' was not found")
        return self._shaders[name]
