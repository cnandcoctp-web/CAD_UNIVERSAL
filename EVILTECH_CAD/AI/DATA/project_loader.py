"""Project-data loaders for the AI pipeline."""

from __future__ import annotations

from pathlib import Path

from IO.project_loader import ProjectLoader


class AIProjectLoader:
    """Load persisted project snapshots for AI processing."""

    def __init__(self) -> None:
        self.loader = ProjectLoader()

    def load(self, project_path: str | Path):
        """Load a project snapshot from disk."""
        return self.loader.load(Path(project_path))
