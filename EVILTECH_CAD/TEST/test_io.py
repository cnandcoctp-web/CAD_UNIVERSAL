"""Regression and integration tests for the EvilTech CAD project system."""

from __future__ import annotations

from pathlib import Path

import pytest

from IO.exporter import ExportManager
from IO.file_manager import (
    AssetRegistry,
    BackupManager,
    FileHistory,
    FileFormatRegistry,
    ProjectManager,
    ProjectValidator,
    RecoveryManager,
)
from IO.importer import ImportManager
from IO.project_loader import ProjectLoader
from IO.project_saver import ProjectSaver


def test_project_manager_creates_expected_project_structure(tmp_path: Path) -> None:
    manager = ProjectManager()

    snapshot = manager.create_new_project(name="Demo Project", root_path=tmp_path / "demo_project")

    assert snapshot.project_path.exists()
    assert (snapshot.project_path / "assets").is_dir()
    assert (snapshot.project_path / "materials").is_dir()
    assert (snapshot.project_path / "simulation_data").is_dir()
    assert (snapshot.project_path / "ai_history").is_dir()
    assert (snapshot.project_path / "configuration").is_dir()
    assert (snapshot.project_path / "logs").is_dir()
    assert (snapshot.project_path / "recovery").is_dir()
    assert snapshot.metadata.name == "Demo Project"


def test_project_save_and_reopen_preserve_data_integrity(tmp_path: Path) -> None:
    manager = ProjectManager()
    snapshot = manager.create_new_project(name="Integrity", root_path=tmp_path / "integrity")
    snapshot.properties["units"] = "mm"
    snapshot.materials = ["Steel"]
    snapshot.asset_registry.register_asset("part-a", "assets/part_a.step")
    manager.save_project(snapshot)

    reopened = manager.open_project(snapshot.project_path)

    assert reopened.metadata.project_id == snapshot.metadata.project_id
    assert reopened.properties["units"] == "mm"
    assert reopened.materials == ["Steel"]
    assert reopened.asset_registry.get_asset("part-a") == "assets/part_a.step"


def test_save_as_and_recent_projects_tracking(tmp_path: Path) -> None:
    manager = ProjectManager()
    snapshot = manager.create_new_project(name="Source", root_path=tmp_path / "source")
    manager.save_project(snapshot)

    cloned = manager.save_project_as(snapshot, tmp_path / "cloned")

    assert cloned.project_path == tmp_path / "cloned"
    assert manager.recent_projects.entries()[0] == str(tmp_path / "cloned")
    assert manager.recent_projects.entries()[1] == str(tmp_path / "source")


def test_autosave_recovery_backup_and_version_history(tmp_path: Path) -> None:
    manager = ProjectManager()
    snapshot = manager.create_new_project(name="Recovery", root_path=tmp_path / "recovery_case")
    snapshot.properties["revision"] = "A"
    manager.save_project(snapshot)
    manager.autosave(snapshot)
    backup_path = manager.backup_manager.create_backup(snapshot)
    recovery_path = manager.recovery_manager.write_recovery_point(snapshot)

    assert backup_path.exists()
    assert recovery_path.exists()
    assert len(snapshot.version_manager.history()) >= 2

    recovered = manager.recovery_manager.restore_latest(snapshot.project_path)
    assert recovered.properties["revision"] == "A"


def test_workspace_session_and_file_history_are_persisted(tmp_path: Path) -> None:
    manager = ProjectManager()
    snapshot = manager.create_new_project(name="Workspace", root_path=tmp_path / "workspace_case")
    snapshot.workspace_state = {"layout": "engineering", "viewports": 2}
    snapshot.session_state = {"last_user": "tester", "active_tools": ["select"]}
    snapshot.file_history.record("created")
    snapshot.file_history.record("saved")
    manager.save_project(snapshot)

    reopened = manager.open_project(snapshot.project_path)

    assert reopened.workspace_state["layout"] == "engineering"
    assert reopened.session_state["last_user"] == "tester"
    assert reopened.file_history.entries() == ["created", "saved"]


def test_import_export_and_format_registry_support_registered_formats(tmp_path: Path) -> None:
    registry = FileFormatRegistry()
    registry.register_format("json", ".json")
    exporter = ExportManager(registry)
    importer = ImportManager(registry)

    payload = {"project": "Demo", "assets": 3}
    export_path = tmp_path / "payload.json"
    exporter.export_data(payload, export_path, "json")
    imported = importer.import_data(export_path, "json")

    assert imported == payload
    assert registry.resolve_extension("json") == ".json"


def test_project_validator_rejects_missing_manifest(tmp_path: Path) -> None:
    validator = ProjectValidator()
    broken = tmp_path / "broken_project"
    broken.mkdir()

    assert validator.validate(broken).is_valid is False


def test_stress_repeated_save_and_load_cycles(tmp_path: Path) -> None:
    manager = ProjectManager()
    snapshot = manager.create_new_project(name="Stress", root_path=tmp_path / "stress_case")
    snapshot.properties["counter"] = 0

    for value in range(10):
        snapshot.properties["counter"] = value
        manager.save_project(snapshot)
        snapshot = manager.open_project(snapshot.project_path)
        assert snapshot.properties["counter"] == value
