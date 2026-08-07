"""Shared constants for the EvilTech CAD foundation layer.

The constants module centralizes the common enumerations and string values
used throughout the foundation services.
"""

from __future__ import annotations

from enum import Enum


APPLICATION_NAME = "EvilTech CAD"
APPLICATION_VERSION = "1.0.0rc1"
RELEASE_TAG = "v1.0.0-rc1"


class LifecycleState(str, Enum):
    """Lifecycle states for runtime objects such as projects and sessions."""

    INITIALIZING = "initializing"
    READY = "ready"
    STARTED = "started"
    OPENED = "opened"
    CREATED = "created"
    INITIALIZED = "initialized"
    ACTIVE = "active"
    CLOSED = "closed"
    STOPPED = "stopped"
    ERROR = "error"


class WorkspaceType(str, Enum):
    """Supported workspace types for the application shell."""

    DEFAULT = "default"
    HOME = "home"
    PROJECT_MANAGER = "project_manager"
    TWO_D = "2d"
    THREE_D = "3d"
    AI = "ai"
    SIMULATION = "simulation"
