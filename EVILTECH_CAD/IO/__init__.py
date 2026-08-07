"""Project management and persistence package for EvilTech CAD."""

from IO.exporter import ExportManager
from IO.file_manager import (
    AssetRegistry,
    BackupManager,
    FileFormatRegistry,
    FileHistory,
    ProjectCreationWizard,
    ProjectManager,
    ProjectMetadata,
    ProjectSnapshot,
    ProjectValidator,
    ProjectVersionManager,
    RecentProjectsManager,
    RecoveryManager,
    SessionRecoveryManager,
    ValidationResult,
    WorkspacePersistenceManager,
)
from IO.importer import ImportManager
from IO.project_loader import ProjectLoader
from IO.project_saver import ProjectSaver

__all__ = [
    "AssetRegistry",
    "BackupManager",
    "ExportManager",
    "FileFormatRegistry",
    "FileHistory",
    "ImportManager",
    "ProjectCreationWizard",
    "ProjectLoader",
    "ProjectManager",
    "ProjectMetadata",
    "ProjectSaver",
    "ProjectSnapshot",
    "ProjectValidator",
    "ProjectVersionManager",
    "RecentProjectsManager",
    "RecoveryManager",
    "SessionRecoveryManager",
    "ValidationResult",
    "WorkspacePersistenceManager",
]