"""Scene graph and scene-management primitives for rendering."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RenderObject:
    """A renderable scene object and its presentation metadata."""

    identifier: str
    geometry: Any
    material_name: str = "default"
    visible: bool = True
    selectable: bool = True
    highlighted: bool = False
    show_bounds: bool = False

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError("identifier must be non-empty")
        if self.geometry is None:
            raise ValueError("geometry must not be None")

    def serialize(self) -> dict[str, Any]:
        """Serialize the render object to a frame-friendly structure."""
        geometry_type = self.geometry.__class__.__name__.lower()
        return {
            "identifier": self.identifier,
            "geometry_type": geometry_type,
            "material_name": self.material_name,
            "visible": self.visible,
            "highlighted": self.highlighted,
            "show_bounds": self.show_bounds,
        }


@dataclass(slots=True)
class SceneGraph:
    """A minimal scene graph containing renderable objects."""

    name: str
    _objects: list[RenderObject] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must be non-empty")

    def add_object(self, render_object: RenderObject) -> None:
        """Add a renderable object to the scene."""
        if not isinstance(render_object, RenderObject):
            raise TypeError("render_object must be a RenderObject")
        if self.find_object(render_object.identifier) is not None:
            raise ValueError(f"Object '{render_object.identifier}' already exists in the scene")
        self._objects.append(render_object)

    def remove_object(self, identifier: str) -> None:
        """Remove a render object by identifier."""
        match = self.find_object(identifier)
        if match is None:
            raise KeyError(f"Object '{identifier}' was not found")
        self._objects.remove(match)

    def object_count(self) -> int:
        """Return the number of renderable objects in the scene."""
        return len(self._objects)

    def find_object(self, identifier: str) -> RenderObject | None:
        """Find an object by identifier."""
        for render_object in self._objects:
            if render_object.identifier == identifier:
                return render_object
        return None

    def visible_objects(self) -> list[RenderObject]:
        """Return the currently visible render objects."""
        return [render_object for render_object in self._objects if render_object.visible]


class SceneManager:
    """Manage one or more scenes and track the active scene."""

    def __init__(self, active_scene: SceneGraph | None = None) -> None:
        self._scenes: dict[str, SceneGraph] = {}
        self.active_scene: SceneGraph | None = None
        if active_scene is not None:
            self.register_scene(active_scene)

    def register_scene(self, scene: SceneGraph) -> None:
        """Register a scene and make it active if none is active yet."""
        if not isinstance(scene, SceneGraph):
            raise TypeError("scene must be a SceneGraph")
        self._scenes[scene.name] = scene
        if self.active_scene is None:
            self.active_scene = scene

    def activate(self, name: str) -> None:
        """Activate a previously registered scene by name."""
        if name not in self._scenes:
            raise KeyError(f"Scene '{name}' was not found")
        self.active_scene = self._scenes[name]

    def scene_names(self) -> list[str]:
        """Return the registered scene names."""
        return list(self._scenes.keys())
