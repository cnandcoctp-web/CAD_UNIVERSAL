"""Lighting primitives for the headless rendering engine."""

from __future__ import annotations

from dataclasses import dataclass

from GEOMETRY.vector import Vector3D


@dataclass(slots=True)
class DirectionalLight:
    """A simple directional light source."""

    identifier: str
    direction: Vector3D
    intensity: float = 1.0

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError("identifier must be non-empty")
        if not isinstance(self.direction, Vector3D):
            raise TypeError("direction must be a Vector3D")
        if self.direction.magnitude() == 0.0:
            raise ValueError("direction must be non-zero")
        if self.intensity <= 0.0:
            raise ValueError("intensity must be positive")


class LightingSystem:
    """Manage active scene lighting definitions."""

    def __init__(self) -> None:
        self._lights: dict[str, DirectionalLight] = {}

    def add_light(self, light: DirectionalLight) -> None:
        """Register a light source."""
        if not isinstance(light, DirectionalLight):
            raise TypeError("light must be a DirectionalLight")
        self._lights[light.identifier] = light

    def light_count(self) -> int:
        """Return the number of active lights."""
        return len(self._lights)

    def serialize(self) -> list[dict[str, object]]:
        """Serialize lights for frame reporting."""
        return [
            {
                "identifier": light.identifier,
                "direction": light.direction.to_dict(),
                "intensity": light.intensity,
            }
            for light in self._lights.values()
        ]
