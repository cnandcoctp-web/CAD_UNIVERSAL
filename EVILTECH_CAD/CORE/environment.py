"""Environment management for the EvilTech CAD foundation layer.

The environment manager resolves runtime values such as the active environment
name from a provided mapping and exposes a stable interface for the rest of the
foundation stack.
"""

from __future__ import annotations

from os import environ
from typing import Mapping, MutableMapping

from CORE.exceptions import EnvironmentError


class EnvironmentManager:
    """Resolve configuration values from a process environment mapping."""

    def __init__(self, env: Mapping[str, str] | None = None) -> None:
        """Initialize the environment manager.

        Args:
            env: Optional environment mapping. If omitted, the process
                environment is used.
        """
        self._env: MutableMapping[str, str] = dict(env or environ)

    def get_environment(self, default: str = "development") -> str:
        """Return the active environment name.

        Args:
            default: The fallback environment if none is configured.

        Returns:
            The resolved environment name.

        Raises:
            EnvironmentError: If the environment value is invalid.
        """
        value = self._env.get("EVILTECH_ENV") or self._env.get("ENV") or default
        if not value or not str(value).strip():
            raise EnvironmentError("Environment value cannot be empty.")
        return str(value)

    def get(self, key: str, default: str | None = None) -> str | None:
        """Return a named environment value.

        Args:
            key: The environment variable name.
            default: The fallback value if the key is absent.

        Returns:
            The configured value or the fallback.
        """
        value = self._env.get(key)
        if value is None:
            return default
        return str(value)
