"""Environment-variable helpers for EvilTech CAD."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class EnvironmentSnapshot:
    """Resolved runtime environment values."""

    environment: str
    log_level: str
    workspace_root: str | None = None


def read_environment() -> EnvironmentSnapshot:
    """Read the current EvilTech-related environment variables."""
    return EnvironmentSnapshot(
        environment=os.environ.get("EVILTECH_ENV", "development"),
        log_level=os.environ.get("EVILTECH_LOG_LEVEL", "INFO"),
        workspace_root=os.environ.get("EVILTECH_WORKSPACE_ROOT"),
    )
