"""Texture management for rendering."""

from __future__ import annotations


class TextureManager:
    """Manage lightweight texture descriptors for the rendering engine."""

    def __init__(self) -> None:
        self._textures: dict[str, object] = {}

    def register_texture(self, name: str, payload: object) -> None:
        """Register a texture payload by name."""
        if not name:
            raise ValueError("name must be non-empty")
        self._textures[name] = payload

    def get_texture(self, name: str) -> object:
        """Return a texture payload by name."""
        if name not in self._textures:
            raise KeyError(f"Texture '{name}' was not found")
        return self._textures[name]
