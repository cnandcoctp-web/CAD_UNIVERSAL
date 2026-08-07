"""Project management and persistence models for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

from CORE.resource_manager import ResourceManager
from IO.project_models import (
    AssetRegistry,
    FileHistory,
    ProjectMetadata,
    ProjectSnapshot,
    ProjectVersionManager,
    RecentProjectsManager,
    ValidationResult,
    _utc_now,
)


class FileFormatRegistry:
    """Register supported import/export formats."""

    def __init__(self) -> None:
        self._formats: dict[str, str] = {}

    def register_format(self, name: str, extension: str) -> None:
        """Register a named file format and its extension."""
        if not name or not extension:
            raise ValueError("name and extension must be non-empty")
        if not extension.startswith("."):
            raise ValueError("extension must start with '.'")
        self._formats[name] = extension

    def resolve_extension(self, name: str) -> str:
        """Return the file extension for a registered format."""
        return self._formats[name]


class ProjectValidator:
    """Validate the presence of required project files and directories."""

    def validate(self, project_path: Path) -> ValidationResult:
        """Validate a project folder against the required storage layout."""
        path = Path(project_path)
        errors: list[str] = []
        manifest = path / "project_metadata.json"
        if not manifest.is_file():
            errors.append("Missing project_metadata.json manifest")
        for required in ("assets", "materials", "simulation_data", "ai_history", "configuration", "logs", "recovery"):
            if not (path / required).is_dir():
                errors.append(f"Missing required directory: {required}")
        return ValidationResult(is_valid=not errors, errors=errors)


class WorkspacePersistenceManager:
    """Manage persisted workspace layout and viewport state."""

    def save(self, snapshot: "ProjectSnapshot", state: dict[str, Any]) -> None:
        """Store workspace state on a project snapshot."""
        snapshot.workspace_state = dict(state)

    def load(self, snapshot: "ProjectSnapshot") -> dict[str, Any]:
        """Return persisted workspace state."""
        return dict(snapshot.workspace_state)


class SessionRecoveryManager:
    """Manage persisted session-recovery state."""

    def save(self, snapshot: "ProjectSnapshot", state: dict[str, Any]) -> None:
        """Store session state on a project snapshot."""
        snapshot.session_state = dict(state)

    def load(self, snapshot: "ProjectSnapshot") -> dict[str, Any]:
        """Return persisted session state."""
        return dict(snapshot.session_state)


class RecoveryManager:
    """Write and restore project recovery points."""

    def __init__(self, saver: "ProjectSaver", loader: "ProjectLoader") -> None:
        self.saver = saver
        self.loader = loader

    def write_recovery_point(self, snapshot: ProjectSnapshot) -> Path:
        """Write a full recovery snapshot to the project's recovery folder."""
        target = snapshot.project_path / "recovery" / f"recovery_v{snapshot.metadata.version}.json"
        self.saver.write_snapshot_file(snapshot, target)
        return target

    def restore_latest(self, project_path: Path) -> ProjectSnapshot:
        """Restore the latest recovery snapshot for a project."""
        recovery_dir = Path(project_path) / "recovery"
        candidates = sorted(recovery_dir.glob("recovery_v*.json"))
        if not candidates:
            raise FileNotFoundError("No recovery snapshots are available")
        return self.loader.load_snapshot_file(candidates[-1])


class BackupManager:
    """Create project backups without modifying live project files."""

    def __init__(self, saver: "ProjectSaver") -> None:
        self.saver = saver

    def create_backup(self, snapshot: ProjectSnapshot) -> Path:
        """Create a serialized backup snapshot in the project's backup folder."""
        target = snapshot.project_path / "backups" / f"backup_v{snapshot.metadata.version}.json"
        self.saver.write_snapshot_file(snapshot, target)
        return target


@dataclass(slots=True)
class ProjectCreationWizard:
    """Headless project-creation wizard for persistence payloads."""

    template_names: list[str] = field(default_factory=lambda: ["default", "mechanical", "civil"])

    def build_payload(self, template_name: str, project_name: str, project_path: Path) -> dict[str, str]:
        """Return a validated project-creation payload."""
        if template_name not in self.template_names:
            raise ValueError(f"Unknown template '{template_name}'")
        if not project_name or not str(project_path):
            raise ValueError("project_name and project_path must be non-empty")
        return {"template": template_name, "name": project_name, "path": str(project_path)}


class ProjectManager:
    """Coordinate project creation, loading, saving, recovery, and history."""

    def __init__(self) -> None:
        from IO.project_loader import ProjectLoader
        from IO.project_saver import ProjectSaver

        self.resource_manager = ResourceManager()
        self.validator = ProjectValidator()
        self.recent_projects = RecentProjectsManager()
        self.workspace_persistence = WorkspacePersistenceManager()
        self.session_recovery = SessionRecoveryManager()
        self.saver = ProjectSaver()
        self.loader = ProjectLoader()
        self.recovery_manager = RecoveryManager(self.saver, self.loader)
        self.backup_manager = BackupManager(self.saver)

    def create_new_project(self, name: str, root_path: Path, description: str = "", properties: dict[str, Any] | None = None) -> ProjectSnapshot:
        """Create a new project snapshot and initialize its folder structure."""
        if not name or not name.strip():
            raise ValueError("name must be a non-empty string")
        metadata = ProjectMetadata(project_id=str(uuid4()), name=name.strip(), description=description)
        snapshot = ProjectSnapshot(metadata=metadata, project_path=Path(root_path), properties=dict(properties or {}))
        snapshot.file_history.record("created")
        snapshot.version_manager.record("created", str(snapshot.project_path))
        self.saver.save(snapshot)
        self._register_project_resource(snapshot)
        self.recent_projects.add(str(snapshot.project_path))
        return snapshot

    def open_project(self, project_path: Path) -> ProjectSnapshot:
        """Load an existing project from disk."""
        result = self.validator.validate(Path(project_path))
        if not result.is_valid:
            raise ValueError("Project validation failed: " + "; ".join(result.errors))
        snapshot = self.loader.load(Path(project_path))
        self._register_project_resource(snapshot)
        self.recent_projects.add(str(snapshot.project_path))
        return snapshot

    def save_project(self, snapshot: ProjectSnapshot) -> Path:
        """Persist a project snapshot to disk."""
        if not isinstance(snapshot, ProjectSnapshot):
            raise TypeError("snapshot must be a ProjectSnapshot")
        snapshot.metadata.updated_at = _utc_now()
        snapshot.metadata.version += 1
        manifest = self.saver.save(snapshot)
        snapshot.file_history.record("saved")
        snapshot.version_manager.record("save", str(manifest))
        self.recent_projects.add(str(snapshot.project_path))
        self._register_project_resource(snapshot)
        return manifest

    def save_project_as(self, snapshot: ProjectSnapshot, target_path: Path) -> ProjectSnapshot:
        """Persist a project snapshot to a new project folder."""
        cloned = snapshot.clone_to(Path(target_path))
        cloned.file_history.record("saved_as")
        self.saver.save(cloned)
        self.recent_projects.add(str(cloned.project_path))
        self._register_project_resource(cloned)
        return cloned

    def autosave(self, snapshot: ProjectSnapshot) -> Path:
        """Write an autosave snapshot to the project's recovery folder."""
        target = self.saver.write_snapshot_file(snapshot, snapshot.project_path / "recovery" / "autosave.json")
        snapshot.file_history.record("autosave")
        snapshot.version_manager.record("autosave", str(target))
        return target

    def _register_project_resource(self, snapshot: ProjectSnapshot) -> None:
        """Register or refresh the project path in the shared resource manager."""
        name = f"project:{snapshot.metadata.project_id}"
        try:
            self.resource_manager.release_resource(name)
        except Exception:
            pass
        self.resource_manager.register_resource(name, str(snapshot.project_path))
