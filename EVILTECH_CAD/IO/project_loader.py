"""Project persistence loader for EvilTech CAD."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from IO.project_models import AssetRegistry, FileHistory, ProjectMetadata, ProjectSnapshot, ProjectVersionManager


class ProjectLoader:
    """Load project snapshots from the project folder structure."""

    def load(self, project_path: Path) -> ProjectSnapshot:
        """Load a project from its canonical folder structure."""
        root = Path(project_path)
        metadata = ProjectMetadata.from_dict(self._read_json(root / "project_metadata.json"))
        snapshot = ProjectSnapshot(
            metadata=metadata,
            project_path=root,
            properties=self._read_json(root / "project_properties.json", default={}),
            materials=self._read_json(root / "materials" / "materials.json", default=[]),
            simulation_data=self._read_json(root / "simulation_data" / "placeholder.json", default={"status": "placeholder"}),
            ai_history=self._read_json(root / "ai_history" / "placeholder.json", default=[]),
            configuration=self._read_json(root / "configuration" / "configuration.json", default={}),
            logs=self._read_json(root / "logs" / "project_logs.json", default=[]),
            workspace_state=self._read_json(root / "configuration" / "workspace.json", default={}),
            session_state=self._read_json(root / "configuration" / "session.json", default={}),
            asset_registry=AssetRegistry(self._read_json(root / "assets" / "registry.json", default={})),
            file_history=FileHistory(self._read_json(root / "logs" / "file_history.json", default=[])),
            version_manager=ProjectVersionManager(self._read_json(root / "versions" / "version_history.json", default=[])),
        )
        return snapshot

    def load_snapshot_file(self, snapshot_path: Path) -> ProjectSnapshot:
        """Load a full serialized recovery or backup snapshot file."""
        payload = self._read_json(Path(snapshot_path))
        return ProjectSnapshot(
            metadata=ProjectMetadata.from_dict(payload["metadata"]),
            project_path=Path(payload["project_path"]),
            properties=dict(payload.get("properties", {})),
            materials=list(payload.get("materials", [])),
            simulation_data=dict(payload.get("simulation_data", {})),
            ai_history=list(payload.get("ai_history", [])),
            configuration=dict(payload.get("configuration", {})),
            logs=list(payload.get("logs", [])),
            workspace_state=dict(payload.get("workspace_state", {})),
            session_state=dict(payload.get("session_state", {})),
            asset_registry=AssetRegistry(dict(payload.get("assets", {}))),
            file_history=FileHistory(list(payload.get("file_history", []))),
            version_manager=ProjectVersionManager(list(payload.get("version_history", []))),
        )

    @staticmethod
    def _read_json(path: Path, default: Any | None = None) -> Any:
        """Read JSON content from disk, returning a default when missing."""
        file_path = Path(path)
        if not file_path.exists():
            if default is not None:
                return default
            raise FileNotFoundError(f"Missing required file: {file_path}")
        with file_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
