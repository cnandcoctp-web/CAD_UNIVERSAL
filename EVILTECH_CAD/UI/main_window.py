"""Application window and workspace primitives for the EvilTech CAD UI framework."""

from __future__ import annotations

from dataclasses import dataclass

from UI.theme import RecentProjectsScreen
from UI.viewport import UIViewportManager


@dataclass(slots=True)
class HomeScreen:
    """Home screen model containing recent-project entry points."""

    recent_projects: RecentProjectsScreen


@dataclass(slots=True)
class ProjectDashboard:
    """Project dashboard model shown after a project is opened."""

    project_name: str
    project_status: str


@dataclass(slots=True)
class MainWorkspace:
    """Main workspace model containing viewports and workspace state."""

    viewports: UIViewportManager

    def render_active_viewport(self) -> dict[str, object]:
        """Render the currently active viewport."""
        if not isinstance(self.viewports, UIViewportManager):
            raise TypeError("viewports must be a UIViewportManager")
        return self.viewports.active_viewport().render_frame()


@dataclass(slots=True)
class ApplicationWindow:
    """Main application window model for the headless UI framework."""

    title: str
    home_screen: HomeScreen
    dashboard: ProjectDashboard
    workspace: MainWorkspace
    is_open: bool = False
    active_screen: str = "home"

    def __post_init__(self) -> None:
        if not self.title:
            raise ValueError("title must be non-empty")

    def launch(self) -> None:
        """Launch the application window."""
        self.is_open = True
        self.active_screen = "home"

    def open_workspace(self) -> None:
        """Switch the active UI to the main workspace."""
        if not self.is_open:
            raise RuntimeError("The application window must be launched before opening the workspace")
        self.active_screen = "workspace"

    def close(self) -> None:
        """Close the application window."""
        self.is_open = False


class WindowManager:
    """Track open application windows."""

    def __init__(self) -> None:
        self._windows: list[ApplicationWindow] = []

    def register(self, window: ApplicationWindow) -> None:
        """Register a window with the manager."""
        if not isinstance(window, ApplicationWindow):
            raise TypeError("window must be an ApplicationWindow")
        self._windows.append(window)

    def window_count(self) -> int:
        """Return the number of tracked windows."""
        return len(self._windows)
