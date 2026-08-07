"""Regression and integration tests for the EvilTech CAD UI framework."""

from __future__ import annotations

import pytest

from GEOMETRY.circle import Circle
from GEOMETRY.line import Line
from GEOMETRY.point import Point3D
from GEOMETRY.vector import Vector3D
from RENDERING.camera import OrthographicCamera
from RENDERING.renderer import RenderContext, RenderPipeline, Renderer
from RENDERING.scene import RenderObject, SceneGraph, SceneManager
from RENDERING.viewport import Viewport as RenderViewport
from RENDERING.viewport import ViewportManager as RenderViewportManager
from UI.command_bar import CommandConsole
from UI.hierarchy_panel import (
    AssetBrowser,
    DockingFramework,
    InspectorPanel,
    LayerManager,
    MaterialBrowser,
    ObjectTree,
    ProjectExplorer,
    WorkspaceLayoutManager,
)
from UI.main_window import ApplicationWindow, HomeScreen, MainWorkspace, ProjectDashboard, WindowManager
from UI.menu_bar import MenuBar, MenuItem
from UI.property_panel import PropertiesPanel, SettingsWindow
from UI.ribbon import RibbonTab, RibbonToolbar
from UI.status_bar import NotificationCenter, ProgressManager, SimulationStatusPanel, StatusBar, TaskManager
from UI.theme import (
    AboutDialog,
    HelpWindow,
    KeyboardShortcutManager,
    LightTheme,
    DarkTheme,
    MouseInputManager,
    NewProjectWizard,
    OpenProjectDialog,
    RecentProjectsScreen,
    SaveProjectDialog,
    ThemeManager,
)
from UI.tool_bar import QuickAccessToolbar, ViewportControls
from UI.viewport import UIViewport, UIViewportManager


def build_renderer() -> Renderer:
    scene = SceneGraph(name="ui-scene")
    scene.add_object(RenderObject(identifier="line-1", geometry=Line(Point3D(0.0, 0.0, 0.0), Point3D(5.0, 0.0, 0.0))))
    scene.add_object(RenderObject(identifier="circle-1", geometry=Circle(Point3D(0.0, 0.0, 0.0), 2.0), show_bounds=True))
    return Renderer(
        context=RenderContext(workspace_mode="2D"),
        scene_manager=SceneManager(scene),
        viewport_manager=RenderViewportManager([RenderViewport(identifier="main", width=1280, height=720)]),
        pipeline=RenderPipeline(),
    )


def build_workspace() -> MainWorkspace:
    renderer = build_renderer()
    camera = OrthographicCamera(
        position=Point3D(0.0, 0.0, 10.0),
        target=Point3D(0.0, 0.0, 0.0),
        up=Vector3D(0.0, 1.0, 0.0),
        width=40.0,
        height=30.0,
    )
    ui_viewport = UIViewport(identifier="main", title="Main View", renderer=renderer, camera=camera)
    return MainWorkspace(viewports=UIViewportManager([ui_viewport]))


def test_application_window_launches_and_navigates_between_home_and_workspace() -> None:
    home = HomeScreen(recent_projects=RecentProjectsScreen(["/tmp/example.etp"]))
    dashboard = ProjectDashboard(project_name="Demo Project", project_status="Ready")
    workspace = build_workspace()
    window = ApplicationWindow(title="EvilTech CAD", home_screen=home, dashboard=dashboard, workspace=workspace)

    window.launch()
    assert window.is_open is True
    assert window.active_screen == "home"

    window.open_workspace()
    assert window.active_screen == "workspace"
    assert window.workspace.viewports.active_viewport().identifier == "main"


def test_menu_ribbon_and_quick_access_toolbars_execute_actions() -> None:
    triggered: list[str] = []
    menu = MenuBar([MenuItem("File", lambda: triggered.append("file")), MenuItem("Help", lambda: triggered.append("help"))])
    ribbon = RibbonToolbar([RibbonTab(name="Home", commands=["Open", "Save"]), RibbonTab(name="View", commands=["Zoom", "Pan"])])
    quick = QuickAccessToolbar(actions={"save": lambda: triggered.append("save"), "undo": lambda: triggered.append("undo")})

    menu.trigger("File")
    menu.trigger("Help")
    quick.invoke("save")

    assert triggered == ["file", "help", "save"]
    assert ribbon.tab_names() == ["Home", "View"]


def test_docking_framework_and_layout_manager_track_panels() -> None:
    docking = DockingFramework()
    docking.dock(ProjectExplorer(["alpha", "beta"]), zone="left")
    docking.dock(ObjectTree(["root", "child"]), zone="left")
    docking.dock(PropertiesPanel({"name": "Part A"}), zone="right")
    docking.dock(InspectorPanel(details={"selection": 2}), zone="right")

    layout = WorkspaceLayoutManager(docking)
    layout.save_layout("default")

    assert docking.panel_count("left") == 2
    assert docking.panel_count("right") == 2
    assert layout.available_layouts() == ["default"]


def test_panels_and_managers_share_state_correctly() -> None:
    layers = LayerManager(["Default", "Hidden"])
    materials = MaterialBrowser(["Steel", "Aluminum"])
    assets = AssetBrowser(["Bolt", "Gear"])
    notifications = NotificationCenter()
    progress = ProgressManager()
    tasks = TaskManager()
    simulation = SimulationStatusPanel(status="idle")

    notifications.publish("Loaded")
    progress.update("render", 0.5)
    tasks.start_task("refresh")
    tasks.complete_task("refresh")
    simulation.set_status("waiting")

    assert layers.layer_count() == 2
    assert materials.item_count() == 2
    assert assets.item_count() == 2
    assert notifications.latest() == "Loaded"
    assert progress.get("render") == pytest.approx(0.5)
    assert tasks.status_of("refresh") == "completed"
    assert simulation.status == "waiting"


def test_viewports_display_rendered_frames_and_controls_update_camera() -> None:
    workspace = build_workspace()
    controls = ViewportControls(workspace.viewports)

    frame = workspace.render_active_viewport()
    controls.zoom_active(-1.0)
    controls.pan_active(2.0, 1.0)

    assert frame["scene_name"] == "ui-scene"
    assert frame["grid"]["visible"] is True
    assert len(frame["renderables"]) == 2


def test_theme_and_input_managers_apply_ui_preferences() -> None:
    themes = ThemeManager(light_theme=LightTheme(), dark_theme=DarkTheme())
    shortcuts = KeyboardShortcutManager()
    mouse = MouseInputManager()

    themes.apply("dark")
    shortcuts.register("open_project", "Ctrl+O")
    mouse.bind("orbit", "middle_drag")

    assert themes.active_theme.name == "dark"
    assert shortcuts.resolve("open_project") == "Ctrl+O"
    assert mouse.resolve("orbit") == "middle_drag"


def test_dialogs_and_help_surfaces_return_expected_payloads() -> None:
    wizard = NewProjectWizard(template_names=["Mechanical", "Civil"])
    opener = OpenProjectDialog(recent_paths=["/tmp/a.etp"])
    saver = SaveProjectDialog(default_extension=".etp")
    about = AboutDialog(product_name="EvilTech CAD", version="0.1.0")
    help_window = HelpWindow(sections=["Getting Started", "Shortcuts"])
    settings = SettingsWindow(values={"theme": "dark"})

    assert wizard.create_project_payload("Mechanical", "Demo")["name"] == "Demo"
    assert opener.open("/tmp/a.etp") == "/tmp/a.etp"
    assert saver.save_as("project") == "project.etp"
    assert about.summary()["product_name"] == "EvilTech CAD"
    assert help_window.section_count() == 2
    assert settings.get("theme") == "dark"


def test_window_manager_tracks_open_windows_and_dashboard_state() -> None:
    manager = WindowManager()
    workspace = build_workspace()
    window = ApplicationWindow(
        title="EvilTech CAD",
        home_screen=HomeScreen(recent_projects=RecentProjectsScreen([])),
        dashboard=ProjectDashboard(project_name="Demo", project_status="Open"),
        workspace=workspace,
    )
    manager.register(window)
    window.launch()

    assert manager.window_count() == 1
    assert window.dashboard.project_status == "Open"