"""Workspace initialization and management for the EvilTech CAD foundation layer.

Workspaces represent the application surfaces that later phases will populate
with domain-specific views and services. The foundation implementation exposes a
small but deterministic lifecycle for workspace creation and activation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional
from uuid import uuid4

from CORE.constants import LifecycleState, WorkspaceType
from CORE.exceptions import WorkspaceError


@dataclass(slots=True)
class Workspace:
    """A workspace object that can be initialized and activated."""

    id: str
    name: str
    workspace_type: WorkspaceType = WorkspaceType.DEFAULT
    state: LifecycleState = LifecycleState.CREATED
    metadata: Dict[str, str] = field(default_factory=dict)


class WorkspaceManager:
    """Create, initialize, activate, and track workspaces."""

    def __init__(self) -> None:
        """Initialize the workspace manager."""
        self._workspaces: Dict[str, Workspace] = {}

    def create_workspace(self, name: str, workspace_type: str | WorkspaceType, metadata: Optional[Dict[str, str]] = None) -> Workspace:
        """Create a new workspace.

        Args:
            name: The workspace name.
            workspace_type: The workspace type name or enum value.
            metadata: Optional metadata for the workspace.

        Returns:
            The created workspace.

        Raises:
            WorkspaceError: If the workspace name or type is invalid.
        """
        if not name or not name.strip():
            raise WorkspaceError("Workspace name must be non-empty.")
        resolved_type = self._coerce_workspace_type(workspace_type)
        workspace = Workspace(id=str(uuid4()), name=name.strip(), workspace_type=resolved_type, metadata=dict(metadata or {}))
        self._workspaces[workspace.id] = workspace
        return workspace

    def initialize_workspace(self, workspace_id: str) -> Workspace:
        """Initialize an existing workspace.

        Args:
            workspace_id: The workspace identifier.

        Returns:
            The updated workspace.

        Raises:
            WorkspaceError: If the workspace does not exist.
        """
        workspace = self._workspaces.get(workspace_id)
        if workspace is None:
            raise WorkspaceError(f"Workspace '{workspace_id}' does not exist.")
        workspace.state = LifecycleState.INITIALIZING
        workspace.state = LifecycleState.INITIALIZED
        return self._clone_workspace(workspace)

    def activate_workspace(self, workspace_id: str) -> Workspace:
        """Activate an existing workspace.

        Args:
            workspace_id: The workspace identifier.

        Returns:
            The updated workspace.

        Raises:
            WorkspaceError: If the workspace does not exist.
        """
        workspace = self._workspaces.get(workspace_id)
        if workspace is None:
            raise WorkspaceError(f"Workspace '{workspace_id}' does not exist.")
        workspace.state = LifecycleState.ACTIVE
        return self._clone_workspace(workspace)

    def get_workspace(self, workspace_id: str) -> Workspace:
        """Retrieve a workspace by identifier."""
        workspace = self._workspaces.get(workspace_id)
        if workspace is None:
            raise WorkspaceError(f"Workspace '{workspace_id}' does not exist.")
        return workspace

    @staticmethod
    def _clone_workspace(workspace: Workspace) -> Workspace:
        """Return a detached copy of a workspace with its current state."""
        return Workspace(
            id=workspace.id,
            name=workspace.name,
            workspace_type=workspace.workspace_type,
            state=workspace.state,
            metadata=dict(workspace.metadata),
        )

    @staticmethod
    def _coerce_workspace_type(value: str | WorkspaceType) -> WorkspaceType:
        """Normalize a workspace type to the ``WorkspaceType`` enum."""
        if isinstance(value, WorkspaceType):
            return value
        try:
            return WorkspaceType(value)
        except ValueError as exc:
            raise WorkspaceError(f"Unsupported workspace type: {value}") from exc
