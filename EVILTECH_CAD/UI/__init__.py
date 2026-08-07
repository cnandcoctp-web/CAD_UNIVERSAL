"""User interface framework package for EvilTech CAD."""

from UI.command_bar import CommandConsole
from UI.hierarchy_panel import (
    AssetBrowser,
    DockPanel,
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
    DarkTheme,
    HelpWindow,
    KeyboardShortcutManager,
    LightTheme,
    MouseInputManager,
    NewProjectWizard,
    OpenProjectDialog,
    RecentProjectsScreen,
    SaveProjectDialog,
    ThemeManager,
)
from UI.tool_bar import QuickAccessToolbar, ViewportControls
from UI.viewport import UIViewport, UIViewportManager

__all__ = [
    "AboutDialog",
    "ApplicationWindow",
    "AssetBrowser",
    "CommandConsole",
    "DarkTheme",
    "DockPanel",
    "DockingFramework",
    "HelpWindow",
    "HomeScreen",
    "InspectorPanel",
    "KeyboardShortcutManager",
    "LayerManager",
    "LightTheme",
    "MainWorkspace",
    "MaterialBrowser",
    "MenuBar",
    "MenuItem",
    "MouseInputManager",
    "NewProjectWizard",
    "NotificationCenter",
    "ObjectTree",
    "OpenProjectDialog",
    "ProgressManager",
    "ProjectDashboard",
    "ProjectExplorer",
    "PropertiesPanel",
    "QuickAccessToolbar",
    "RecentProjectsScreen",
    "RibbonTab",
    "RibbonToolbar",
    "SaveProjectDialog",
    "SettingsWindow",
    "SimulationStatusPanel",
    "StatusBar",
    "TaskManager",
    "ThemeManager",
    "UIViewport",
    "UIViewportManager",
    "ViewportControls",
    "WindowManager",
    "WorkspaceLayoutManager",
]