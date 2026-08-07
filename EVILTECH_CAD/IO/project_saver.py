"""Project persistence writer for EvilTech CAD."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from IO.project_models import ProjectSnapshot


class ProjectSaver:
    """Persist project snapshots to the project folder structure."""

    REQUIRED_DIRECTORIES = (
        "assets",
        "materials",
        "simulation_data",
        "ai_history",
        "configuration",
        "logs",
        "recovery",
        "backups",
        "versions",
    )

    def initialize_project_structure(self, project_path: Path) -> None:
        """Ensure the required project directories exist."""
        path = Path(project_path)
        path.mkdir(parents=True, exist_ok=True)
        for directory in self.REQUIRED_DIRECTORIES:
            (path / directory).mkdir(parents=True, exist_ok=True)

    def save(self, snapshot: ProjectSnapshot) -> Path:
        """Persist a project snapshot into its folder structure."""
        if not isinstance(snapshot, ProjectSnapshot):
            raise TypeError("snapshot must be a ProjectSnapshot")
        self.initialize_project_structure(snapshot.project_path)
        self._write_json(snapshot.project_path / "project_metadata.json", snapshot.metadata.to_dict())
        self._write_json(snapshot.project_path / "project_properties.json", snapshot.properties)
        self._write_json(snapshot.project_path / "assets" / "registry.json", snapshot.asset_registry.to_dict())
        self._write_json(snapshot.project_path / "materials" / "materials.json", snapshot.materials)
        self._write_json(snapshot.project_path / "simulation_data" / "placeholder.json", snapshot.simulation_data)
        self._write_json(snapshot.project_path / "ai_history" / "placeholder.json", snapshot.ai_history)
        self._write_json(snapshot.project_path / "configuration" / "configuration.json", snapshot.configuration)
        self._write_json(snapshot.project_path / "configuration" / "workspace.json", snapshot.workspace_state)
        self._write_json(snapshot.project_path / "configuration" / "session.json", snapshot.session_state)
        self._write_json(snapshot.project_path / "logs" / "project_logs.json", snapshot.logs)
        self._write_json(snapshot.project_path / "logs" / "file_history.json", snapshot.file_history.entries())
        self._write_json(snapshot.project_path / "versions" / "version_history.json", snapshot.version_manager.history())
        return snapshot.project_path / "project_metadata.json"

    def write_snapshot_file(self, snapshot: ProjectSnapshot, target_path: Path) -> Path:
        """Write a full snapshot payload to an arbitrary JSON file."""
        target = Path(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "metadata": snapshot.metadata.to_dict(),
            "properties": snapshot.properties,
            "assets": snapshot.asset_registry.to_dict(),
            "materials": snapshot.materials,
            "simulation_data": snapshot.simulation_data,
            "ai_history": snapshot.ai_history,
            "configuration": snapshot.configuration,
            "logs": snapshot.logs,
            "workspace_state": snapshot.workspace_state,
            "session_state": snapshot.session_state,
            "file_history": snapshot.file_history.entries(),
            "version_history": snapshot.version_manager.history(),
            "project_path": str(snapshot.project_path),
        }
        self._write_json(target, payload)
        return target

    @staticmethod
    def _write_json(path: Path, payload: Any) -> None:
        """Write JSON content to disk with deterministic formatting."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with Path(path).open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
