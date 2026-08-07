"""Headless renderer and render pipeline for EvilTech CAD."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from GEOMETRY.circle import Circle
from GEOMETRY.line import Line
from GEOMETRY.point import Point3D
from GEOMETRY.topology import BoundingBox
from RENDERING.camera import BaseCamera
from RENDERING.lighting import LightingSystem
from RENDERING.materials import Material, MaterialLibrary
from RENDERING.overlays import OverlayRenderer
from RENDERING.scene import RenderObject, SceneManager
from RENDERING.shaders import ShaderManager
from RENDERING.textures import TextureManager
from RENDERING.viewport import ViewportManager


@dataclass(slots=True)
class RenderContext:
    """Rendering context and engine configuration."""

    workspace_mode: str
    frame_index: int = 0
    smooth_updates: bool = True

    def __post_init__(self) -> None:
        if self.workspace_mode not in {"2D", "3D"}:
            raise ValueError("workspace_mode must be '2D' or '3D'")


class RenderPipeline:
    """Generate frame data for the headless rendering engine."""

    def build_frame(
        self,
        scene_manager: SceneManager,
        viewport_manager: ViewportManager,
        camera: BaseCamera,
        overlays: OverlayRenderer,
        lighting: LightingSystem,
        materials: MaterialLibrary,
    ) -> dict[str, Any]:
        """Construct a serializable frame representation."""
        if scene_manager.active_scene is None:
            raise ValueError("An active scene is required to render")
        renderables: list[dict[str, Any]] = []
        highlighted_ids: list[str] = []
        selection_ids: list[str] = []
        bounds: list[BoundingBox] = []
        for render_object in scene_manager.active_scene.visible_objects():
            item = render_object.serialize()
            item["viewport_ids"] = [viewport.identifier for viewport in viewport_manager.all()]
            item["visible"] = self._is_visible(render_object, camera)
            renderables.append(item)
            if render_object.highlighted:
                highlighted_ids.append(render_object.identifier)
            if render_object.show_bounds:
                bounds.append(self._build_bounds(render_object.geometry))
        overlay_frame = overlays.render(selection_ids=selection_ids, highlighted_ids=highlighted_ids, bounding_boxes=bounds)
        overlay_items = overlay_frame.pop("bounding_boxes")
        return {
            "scene_name": scene_manager.active_scene.name,
            "camera": {
                "position": scene_manager.active_scene.name and camera.position.to_dict(),
                "target": camera.target.to_dict(),
                "projection": camera.projection_state(),
            },
            "grid": {"visible": True, "spacing": 1.0},
            "axis": {"visible": True, "axes": ["x", "y", "z"]},
            "renderables": renderables,
            "overlays": overlay_items,
            "overlay_state": overlay_frame,
            "lights": lighting.serialize(),
            "materials": list(materials._materials.keys()),
        }

    def _is_visible(self, render_object: RenderObject, camera: BaseCamera) -> bool:
        """Determine whether an object is visible for the active camera."""
        geometry = render_object.geometry
        if isinstance(geometry, Circle):
            return geometry.radius >= 0.0
        if isinstance(geometry, Line):
            return geometry.length() >= 0.0
        return True

    def _build_bounds(self, geometry: object) -> BoundingBox:
        """Build a simple bounding box from known geometry types."""
        if isinstance(geometry, Circle):
            center = geometry.center
            radius = geometry.radius
            return BoundingBox([
                Point3D(center.x - radius, center.y - radius, center.z - radius),
                Point3D(center.x + radius, center.y + radius, center.z + radius),
            ])
        if isinstance(geometry, Line):
            return BoundingBox([geometry.start, geometry.end])
        raise TypeError(f"Bounding box generation is not supported for {geometry.__class__.__name__}")


class Renderer:
    """Coordinate render subsystems and generate headless frame outputs."""

    def __init__(
        self,
        context: RenderContext,
        scene_manager: SceneManager,
        viewport_manager: ViewportManager,
        pipeline: RenderPipeline,
        lighting: LightingSystem | None = None,
        materials: MaterialLibrary | None = None,
        textures: TextureManager | None = None,
        shaders: ShaderManager | None = None,
        overlays: OverlayRenderer | None = None,
    ) -> None:
        if not isinstance(context, RenderContext):
            raise TypeError("context must be a RenderContext")
        if not isinstance(scene_manager, SceneManager):
            raise TypeError("scene_manager must be a SceneManager")
        if not isinstance(viewport_manager, ViewportManager):
            raise TypeError("viewport_manager must be a ViewportManager")
        if not isinstance(pipeline, RenderPipeline):
            raise TypeError("pipeline must be a RenderPipeline")
        self.context = context
        self.scene_manager = scene_manager
        self.viewport_manager = viewport_manager
        self.pipeline = pipeline
        self.lighting = lighting or LightingSystem()
        self.materials = materials or MaterialLibrary()
        self.textures = textures or TextureManager()
        self.shaders = shaders or ShaderManager()
        self.overlays = overlays or OverlayRenderer()
        if "default" not in self.materials._materials:
            self.materials.register(Material(name="default", color=(0.8, 0.8, 0.8), opacity=1.0))

    def render(self, camera: BaseCamera) -> dict[str, Any]:
        """Render the active scene to a serializable frame representation."""
        if not isinstance(camera, BaseCamera):
            raise TypeError("camera must be a BaseCamera")
        frame = self.pipeline.build_frame(
            scene_manager=self.scene_manager,
            viewport_manager=self.viewport_manager,
            camera=camera,
            overlays=self.overlays,
            lighting=self.lighting,
            materials=self.materials,
        )
        frame["frame_index"] = self.context.frame_index
        frame["delta_time"] = 1.0 / 60.0 if self.context.smooth_updates else 0.0
        self.context.frame_index += 1
        return frame

    def pick(self, viewport_id: str, x: int, y: int, camera: BaseCamera) -> str | None:
        """Return the first visible selectable object under a viewport coordinate."""
        viewport = self.viewport_manager.get(viewport_id)
        if not viewport.contains(x, y):
            return None
        if self.scene_manager.active_scene is None:
            return None
        for render_object in self.scene_manager.active_scene.visible_objects():
            if render_object.selectable and self.pipeline._is_visible(render_object, camera):
                return render_object.identifier
        return None


@dataclass(slots=True)
class RenderLoop:
    """Execute repeated render passes for smooth frame updates."""

    renderer: Renderer
    target_frame_rate: int = 60

    def __post_init__(self) -> None:
        if not isinstance(self.renderer, Renderer):
            raise TypeError("renderer must be a Renderer")
        if self.target_frame_rate <= 0:
            raise ValueError("target_frame_rate must be positive")

    def run(self, camera: BaseCamera, frame_count: int) -> list[dict[str, Any]]:
        """Render a bounded number of frames."""
        if not isinstance(frame_count, int) or frame_count <= 0:
            raise ValueError("frame_count must be a positive integer")
        frames: list[dict[str, Any]] = []
        for _ in range(frame_count):
            frame = self.renderer.render(camera)
            frame["delta_time"] = min(frame["delta_time"], 1.0 / float(self.target_frame_rate))
            frames.append(frame)
        return frames
