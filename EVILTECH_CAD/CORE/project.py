"""Project lifecycle management for the EvilTech CAD foundation layer.

The project lifecycle manager provides the canonical state transitions for a
project and ensures that projects move through explicit lifecycle states.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional
from uuid import uuid4

from CORE.constants import LifecycleState
from CORE.exceptions import ProjectError


@dataclass(slots=True)
class Project:
    """A lightweight project record used by the foundation services."""

    id: str
    name: str
    lifecycle_state: LifecycleState = LifecycleState.CREATED
    metadata: Dict[str, str] = field(default_factory=dict)


class ProjectLifecycleManager:
    """Create, open, close, and track project lifecycle state."""

    def __init__(self) -> None:
        """Initialize the project lifecycle manager."""
        self._projects: Dict[str, Project] = {}

    def create_project(self, name: str, metadata: Optional[Dict[str, str]] = None) -> Project:
        """Create a new project with a generated identifier.

        Args:
            name: The human-readable project name.
            metadata: Optional metadata to attach to the project.

        Returns:
            The newly created project.

        Raises:
            ProjectError: If the project name is invalid.
        """
        if not name or not name.strip():
            raise ProjectError("Project name must be non-empty.")
        project = Project(id=str(uuid4()), name=name.strip(), metadata=dict(metadata or {}))
        self._projects[project.id] = project
        return project

    def open_project(self, project_id: str) -> Project:
        """Open an existing project and transition it to the opened state.

        Args:
            project_id: The project identifier.

        Returns:
            The updated project.

        Raises:
            ProjectError: If the project does not exist.
        """
        project = self._projects.get(project_id)
        if project is None:
            raise ProjectError(f"Project '{project_id}' does not exist.")
        project.lifecycle_state = LifecycleState.OPENED
        return project

    def close_project(self, project_id: str) -> Project:
        """Close an existing project and transition it to the closed state.

        Args:
            project_id: The project identifier.

        Returns:
            The updated project.

        Raises:
            ProjectError: If the project does not exist.
        """
        project = self._projects.get(project_id)
        if project is None:
            raise ProjectError(f"Project '{project_id}' does not exist.")
        project.lifecycle_state = LifecycleState.CLOSED
        return project

    def get_project(self, project_id: str) -> Project:
        """Return a project by identifier."""
        project = self._projects.get(project_id)
        if project is None:
            raise ProjectError(f"Project '{project_id}' does not exist.")
        return project
