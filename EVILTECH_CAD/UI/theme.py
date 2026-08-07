"""Theme, input, and dialog primitives for the EvilTech CAD UI framework."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class BaseTheme:
    """Base theme model."""

    name: str
    palette: dict[str, str]


class LightTheme(BaseTheme):
    """Light UI theme."""

    def __init__(self) -> None:
        super().__init__(name="light", palette={"background": "#f4f6f8", "foreground": "#0f172a"})


class DarkTheme(BaseTheme):
    """Dark UI theme."""

    def __init__(self) -> None:
        super().__init__(name="dark", palette={"background": "#0f172a", "foreground": "#e2e8f0"})


class ThemeManager:
    """Apply and track active UI themes."""

    def __init__(self, light_theme: LightTheme, dark_theme: DarkTheme) -> None:
        self._themes = {light_theme.name: light_theme, dark_theme.name: dark_theme}
        self.active_theme: BaseTheme = light_theme

    def apply(self, name: str) -> None:
        """Activate a named theme."""
        if name not in self._themes:
            raise KeyError(f"Theme '{name}' was not found")
        self.active_theme = self._themes[name]


class KeyboardShortcutManager:
    """Manage keyboard shortcut bindings."""

    def __init__(self) -> None:
        self._bindings: dict[str, str] = {}

    def register(self, command: str, shortcut: str) -> None:
        """Register a keyboard shortcut for a command."""
        self._bindings[command] = shortcut

    def resolve(self, command: str) -> str:
        """Resolve a keyboard shortcut by command name."""
        return self._bindings[command]


class MouseInputManager:
    """Manage mouse gesture bindings."""

    def __init__(self) -> None:
        self._bindings: dict[str, str] = {}

    def bind(self, action: str, gesture: str) -> None:
        """Bind a gesture to an action."""
        self._bindings[action] = gesture

    def resolve(self, action: str) -> str:
        """Resolve a gesture by action name."""
        return self._bindings[action]


@dataclass(slots=True)
class RecentProjectsScreen:
    """Recent projects screen shown on the home page."""

    recent_paths: list[str] = field(default_factory=list)


@dataclass(slots=True)
class NewProjectWizard:
    """Wizard model for creating new projects."""

    template_names: list[str] = field(default_factory=list)

    def create_project_payload(self, template_name: str, project_name: str) -> dict[str, str]:
        """Return a validated new-project payload."""
        if template_name not in self.template_names:
            raise ValueError(f"Unknown template '{template_name}'")
        if not project_name:
            raise ValueError("project_name must be non-empty")
        return {"template": template_name, "name": project_name}


@dataclass(slots=True)
class OpenProjectDialog:
    """Dialog model for opening projects."""

    recent_paths: list[str] = field(default_factory=list)

    def open(self, path: str) -> str:
        """Return the selected project path."""
        if not isinstance(path, str) or not path.strip():
            raise ValueError("path must be a non-empty string")
        return path


@dataclass(slots=True)
class SaveProjectDialog:
    """Dialog model for saving projects."""

    default_extension: str = ".etp"

    def save_as(self, path: str) -> str:
        """Return a normalized save path with the default extension."""
        if not isinstance(path, str) or not path.strip():
            raise ValueError("path must be a non-empty string")
        return path if path.endswith(self.default_extension) else f"{path}{self.default_extension}"


@dataclass(slots=True)
class AboutDialog:
    """About dialog model."""

    product_name: str
    version: str

    def summary(self) -> dict[str, str]:
        """Return a serializable about dialog summary."""
        return {"product_name": self.product_name, "version": self.version}


@dataclass(slots=True)
class HelpWindow:
    """Help window model."""

    sections: list[str] = field(default_factory=list)

    def section_count(self) -> int:
        """Return the number of help sections."""
        return len(self.sections)
