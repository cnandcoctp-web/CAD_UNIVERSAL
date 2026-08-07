"""Shared persistence models for the EvilTech CAD IO package."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now() -> str:
    """Return a UTC ISO-8601 timestamp."""
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class ProjectMetadata:
    """Serializable metadata describing a persisted engineering project."""

    project_id: str
    name: str
    description: str = ""
    created_at: str = field(default_factory=_utc_now)
    updated_at: str = field(default_factory=_utc_now)
    version: int = 1

    def __post_init__(self) -> None:
        if not self.project_id:
            raise ValueError("project_id must be non-empty")
        if not self.name or not self.name.strip():
            raise ValueError("name must be non-empty")
        if self.version <= 0:
            raise ValueError("version must be positive")

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable representation of the metadata."""
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ProjectMetadata":
        """Create metadata from a dictionary payload."""
        return cls(
            project_id=str(payload["project_id"]),
            name=str(payload["name"]),
            description=str(payload.get("description", "")),
            created_at=str(payload.get("created_at", _utc_now())),
            updated_at=str(payload.get("updated_at", _utc_now())),
            version=int(payload.get("version", 1)),
        )


class AssetRegistry:
    """Track project asset identifiers and relative paths."""

    def __init__(self, assets: dict[str, str] | None = None) -> None:
        self._assets: dict[str, str] = dict(assets or {})

    def register_asset(self, identifier: str, relative_path: str) -> None:
        """Register or update an asset path."""
        if not identifier or not relative_path:
            raise ValueError("identifier and relative_path must be non-empty")
        self._assets[identifier] = relative_path

    def get_asset(self, identifier: str) -> str:
        """Return the registered path for an asset."""
        return self._assets[identifier]

    def to_dict(self) -> dict[str, str]:
        """Return the serialized asset mapping."""
        return dict(self._assets)


class FileHistory:
    """Maintain a chronological history of project file operations."""

    def __init__(self, items: list[str] | None = None) -> None:
        self._items: list[str] = list(items or [])

    def record(self, event: str) -> None:
        """Record a new file-history event."""
        if not event or not event.strip():
            raise ValueError("event must be a non-empty string")
        if self._items and self._items[-1] == event:
            return
        self._items.append(event)

    def entries(self) -> list[str]:
        """Return the recorded file-history events."""
        return list(self._items)


class ProjectVersionManager:
    """Track version-history events for a project."""

    def __init__(self, items: list[dict[str, Any]] | None = None) -> None:
        self._items: list[dict[str, Any]] = list(items or [])

    def record(self, event: str, path: str) -> None:
        """Record a version event."""
        if not event or not path:
            raise ValueError("event and path must be non-empty")
        self._items.append({"event": event, "path": path, "timestamp": _utc_now()})

    def history(self) -> list[dict[str, Any]]:
        """Return the version-history records."""
        return list(self._items)


class RecentProjectsManager:
    """Track recently opened or saved projects."""

    def __init__(self) -> None:
        self._entries: list[str] = []

    def add(self, project_path: str) -> None:
        """Move a project path to the front of the recent-projects list."""
        if not project_path:
            raise ValueError("project_path must be non-empty")
        if project_path in self._entries:
            self._entries.remove(project_path)
        self._entries.insert(0, project_path)

    def entries(self) -> list[str]:
        """Return recent project paths in newest-first order."""
        return list(self._entries)


@dataclass(slots=True)
class ValidationResult:
    """Validation result for a project folder."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ProjectSnapshot:
    """Full persisted project state used by the IO system."""

    metadata: ProjectMetadata
    project_path: Path
    properties: dict[str, Any] = field(default_factory=dict)
    materials: list[str] = field(default_factory=list)
    simulation_data: dict[str, Any] = field(default_factory=lambda: {"status": "placeholder"})
    ai_history: list[dict[str, Any]] = field(default_factory=list)
    configuration: dict[str, Any] = field(default_factory=lambda: {"cloud_sync": "future", "team_collaboration": "future"})
    logs: list[str] = field(default_factory=list)
    workspace_state: dict[str, Any] = field(default_factory=dict)
    session_state: dict[str, Any] = field(default_factory=dict)
    asset_registry: AssetRegistry = field(default_factory=AssetRegistry)
    file_history: FileHistory = field(default_factory=FileHistory)
    version_manager: ProjectVersionManager = field(default_factory=ProjectVersionManager)

    def __post_init__(self) -> None:
        self.project_path = Path(self.project_path)
        if not isinstance(self.metadata, ProjectMetadata):
            raise TypeError("metadata must be a ProjectMetadata")

    def clone_to(self, project_path: Path) -> "ProjectSnapshot":
        """Return a copy of the snapshot targeting a new project path."""
        return ProjectSnapshot(
            metadata=ProjectMetadata.from_dict(self.metadata.to_dict()),
            project_path=Path(project_path),
            properties=dict(self.properties),
            materials=list(self.materials),
            simulation_data=dict(self.simulation_data),
            ai_history=list(self.ai_history),
            configuration=dict(self.configuration),
            logs=list(self.logs),
            workspace_state=dict(self.workspace_state),
            session_state=dict(self.session_state),
            asset_registry=AssetRegistry(self.asset_registry.to_dict()),
            file_history=FileHistory(self.file_history.entries()),
            version_manager=ProjectVersionManager(self.version_manager.history()),
        )