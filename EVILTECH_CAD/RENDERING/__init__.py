"""Rendering engine package for EvilTech CAD."""

from RENDERING.camera import CameraController, OrthographicCamera, PerspectiveCamera
from RENDERING.lighting import DirectionalLight, LightingSystem
from RENDERING.materials import Material, MaterialLibrary
from RENDERING.overlays import BackgroundSystem, CoordinateGizmo, OverlayRenderer
from RENDERING.renderer import RenderContext, RenderLoop, RenderPipeline, Renderer
from RENDERING.scene import RenderObject, SceneGraph, SceneManager
from RENDERING.shaders import ShaderManager
from RENDERING.textures import TextureManager
from RENDERING.viewport import Viewport, ViewportManager

__all__ = [
    "BackgroundSystem",
    "CameraController",
    "CoordinateGizmo",
    "DirectionalLight",
    "LightingSystem",
    "Material",
    "MaterialLibrary",
    "OrthographicCamera",
    "OverlayRenderer",
    "PerspectiveCamera",
    "RenderContext",
    "RenderLoop",
    "RenderObject",
    "RenderPipeline",
    "Renderer",
    "SceneGraph",
    "SceneManager",
    "ShaderManager",
    "TextureManager",
    "Viewport",
    "ViewportManager",
]