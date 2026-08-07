"""Regression and integration tests for the EvilTech CAD rendering engine."""

from __future__ import annotations

import math

import pytest

from GEOMETRY.circle import Circle
from GEOMETRY.line import Line
from GEOMETRY.point import Point3D
from GEOMETRY.topology import BoundingBox
from GEOMETRY.vector import Vector3D
from RENDERING.camera import CameraController, OrthographicCamera, PerspectiveCamera
from RENDERING.lighting import DirectionalLight, LightingSystem
from RENDERING.materials import Material, MaterialLibrary
from RENDERING.overlays import BackgroundSystem, CoordinateGizmo, OverlayRenderer
from RENDERING.renderer import RenderContext, RenderLoop, RenderPipeline, Renderer
from RENDERING.scene import RenderObject, SceneGraph, SceneManager
from RENDERING.shaders import ShaderManager
from RENDERING.textures import TextureManager
from RENDERING.viewport import Viewport, ViewportManager


def test_scene_graph_and_manager_store_renderables() -> None:
    scene = SceneGraph(name="main")
    object_a = RenderObject(identifier="line-1", geometry=Line(Point3D(0.0, 0.0, 0.0), Point3D(1.0, 0.0, 0.0)))
    object_b = RenderObject(identifier="circle-1", geometry=Circle(Point3D(0.0, 0.0, 0.0), 1.0))

    scene.add_object(object_a)
    scene.add_object(object_b)

    manager = SceneManager()
    manager.register_scene(scene)

    assert manager.active_scene is scene
    assert scene.object_count() == 2
    assert scene.find_object("circle-1") is object_b


def test_camera_controller_supports_zoom_pan_orbit_and_rotate() -> None:
    camera = PerspectiveCamera(position=Point3D(0.0, 0.0, 10.0), target=Point3D(0.0, 0.0, 0.0), up=Vector3D(0.0, 1.0, 0.0), field_of_view=60.0, aspect_ratio=1.6)
    controller = CameraController(camera)

    controller.zoom(-2.0)
    controller.pan(1.0, -1.0)
    controller.rotate(yaw_degrees=90.0, pitch_degrees=0.0)
    controller.orbit(yaw_degrees=0.0, pitch_degrees=45.0)

    assert camera.position.z < 10.0
    assert camera.target.x == pytest.approx(1.0)
    assert camera.target.y == pytest.approx(-1.0)
    assert controller.view_direction().magnitude() == pytest.approx(1.0)


def test_orthographic_camera_resize_updates_projection_state() -> None:
    camera = OrthographicCamera(position=Point3D(0.0, 0.0, 10.0), target=Point3D(0.0, 0.0, 0.0), up=Vector3D(0.0, 1.0, 0.0), width=20.0, height=10.0)
    camera.resize(width=40.0, height=20.0)

    projection = camera.projection_state()
    assert projection["width"] == pytest.approx(40.0)
    assert projection["height"] == pytest.approx(20.0)


def test_render_pipeline_renders_empty_scene_and_grid() -> None:
    context = RenderContext(workspace_mode="3D")
    scene = SceneGraph(name="empty")
    manager = SceneManager(scene)
    viewport = Viewport(identifier="primary", width=1280, height=720)
    camera = PerspectiveCamera(position=Point3D(0.0, 0.0, 10.0), target=Point3D(0.0, 0.0, 0.0), up=Vector3D(0.0, 1.0, 0.0), field_of_view=60.0, aspect_ratio=1280 / 720)
    pipeline = RenderPipeline()
    renderer = Renderer(context=context, scene_manager=manager, viewport_manager=ViewportManager([viewport]), pipeline=pipeline)

    frame = renderer.render(camera=camera)

    assert frame["scene_name"] == "empty"
    assert frame["grid"]["visible"] is True
    assert frame["renderables"] == []


def test_renderer_renders_geometry_primitives_and_bounding_boxes() -> None:
    scene = SceneGraph(name="geometry")
    scene.add_object(RenderObject(identifier="line-1", geometry=Line(Point3D(0.0, 0.0, 0.0), Point3D(2.0, 0.0, 0.0))))
    scene.add_object(RenderObject(identifier="circle-1", geometry=Circle(Point3D(0.0, 0.0, 0.0), 1.0), show_bounds=True))

    renderer = Renderer(
        context=RenderContext(workspace_mode="2D"),
        scene_manager=SceneManager(scene),
        viewport_manager=ViewportManager([Viewport(identifier="draft", width=800, height=600)]),
        pipeline=RenderPipeline(),
    )

    frame = renderer.render(camera=OrthographicCamera(position=Point3D(0.0, 0.0, 10.0), target=Point3D(0.0, 0.0, 0.0), up=Vector3D(0.0, 1.0, 0.0), width=20.0, height=15.0))

    identifiers = [item["identifier"] for item in frame["renderables"]]
    assert identifiers == ["line-1", "circle-1"]
    assert any(item["type"] == "bounding_box" for item in frame["overlays"])


def test_render_subsystems_manage_lights_materials_textures_and_shaders() -> None:
    lighting = LightingSystem()
    lighting.add_light(DirectionalLight(identifier="sun", direction=Vector3D(0.0, -1.0, -1.0), intensity=2.0))

    materials = MaterialLibrary()
    materials.register(Material(name="default", color=(0.8, 0.8, 0.8), opacity=1.0))

    textures = TextureManager()
    textures.register_texture("grid", {"pattern": "lines"})

    shaders = ShaderManager()
    shaders.register_shader("flat", {"passes": ["base"]})

    assert lighting.light_count() == 1
    assert materials.get("default").opacity == pytest.approx(1.0)
    assert textures.get_texture("grid")["pattern"] == "lines"
    assert shaders.get_shader("flat")["passes"] == ["base"]


def test_overlay_renderer_and_background_system_generate_overlay_frame() -> None:
    overlays = OverlayRenderer(background=BackgroundSystem(style="gradient", primary_color="#0f172a", secondary_color="#1e293b"), gizmo=CoordinateGizmo(size=48))
    bbox = BoundingBox([Point3D(-1.0, -1.0, -1.0), Point3D(1.0, 1.0, 1.0)])

    frame = overlays.render(selection_ids=["circle-1"], highlighted_ids=["line-1"], bounding_boxes=[bbox])

    assert frame["background"]["style"] == "gradient"
    assert frame["selection"] == ["circle-1"]
    assert frame["highlight"] == ["line-1"]
    assert frame["gizmo"]["axes"] == ["x", "y", "z"]


def test_render_loop_produces_smooth_frame_updates() -> None:
    renderer = Renderer(
        context=RenderContext(workspace_mode="3D"),
        scene_manager=SceneManager(SceneGraph(name="loop")),
        viewport_manager=ViewportManager([Viewport(identifier="primary", width=640, height=480)]),
        pipeline=RenderPipeline(),
    )
    camera = PerspectiveCamera(position=Point3D(0.0, 0.0, 8.0), target=Point3D(0.0, 0.0, 0.0), up=Vector3D(0.0, 1.0, 0.0), field_of_view=45.0, aspect_ratio=640 / 480)
    loop = RenderLoop(renderer=renderer, target_frame_rate=60)

    frames = loop.run(camera=camera, frame_count=3)

    assert len(frames) == 3
    assert all(frame["frame_index"] >= 0 for frame in frames)
    assert all(frame["delta_time"] <= (1.0 / 60.0) * 1.2 for frame in frames)


def test_render_validation_reports_visible_geometry_and_picking() -> None:
    scene = SceneGraph(name="validation")
    scene.add_object(RenderObject(identifier="circle-1", geometry=Circle(Point3D(0.0, 0.0, 0.0), 2.0), material_name="default"))
    renderer = Renderer(
        context=RenderContext(workspace_mode="2D"),
        scene_manager=SceneManager(scene),
        viewport_manager=ViewportManager([Viewport(identifier="qa", width=400, height=400)]),
        pipeline=RenderPipeline(),
    )
    camera = OrthographicCamera(position=Point3D(0.0, 0.0, 10.0), target=Point3D(0.0, 0.0, 0.0), up=Vector3D(0.0, 1.0, 0.0), width=20.0, height=20.0)

    frame = renderer.render(camera=camera)
    picked = renderer.pick(viewport_id="qa", x=200, y=200, camera=camera)

    assert frame["renderables"][0]["visible"] is True
    assert picked == "circle-1"
