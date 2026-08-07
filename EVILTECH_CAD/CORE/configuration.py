"""Configuration loading for the EvilTech CAD foundation layer.

This module provides a typed configuration model and a loader that resolves
values from a JSON file and an optional environment mapping. It is designed to
be explicit, defensive, and suitable for future expansion.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from CORE.exceptions import ConfigurationError


@dataclass(slots=True)
class ApplicationConfiguration:
    """Typed application configuration values."""

    app_name: str = "EvilTech CAD"
    environment: str = "development"
    log_level: str = "INFO"
    workspace_root: str | None = None


class ConfigurationLoader:
    """Load and validate application configuration from a file or mapping."""

    def load(self, path: str | Path, env: Mapping[str, str] | None = None) -> ApplicationConfiguration:
        """Load configuration from a JSON file.

        Args:
            path: The configuration file path.
            env: Optional environment values that override config defaults.

        Returns:
            A validated configuration object.

        Raises:
            ConfigurationError: If the file cannot be read or the configuration
                is invalid.
        """
        config_path = Path(path)
        if not config_path.exists():
            raise ConfigurationError(f"Configuration file not found: {config_path}")

        try:
            with config_path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except json.JSONDecodeError as exc:
            raise ConfigurationError(f"Invalid JSON configuration: {config_path}") from exc

        return self.load_from_mapping(payload, env=env)

    def load_from_mapping(self, payload: Mapping[str, Any], env: Mapping[str, str] | None = None) -> ApplicationConfiguration:
        """Load configuration from an in-memory mapping.

        Args:
            payload: A mapping containing config values.
            env: Optional environment overrides.

        Returns:
            A validated configuration object.

        Raises:
            ConfigurationError: If the configuration payload is invalid.
        """
        if not isinstance(payload, Mapping):
            raise ConfigurationError("Configuration payload must be a mapping.")

        resolved_env = env or {}
        app_name = self._require_string(payload, "app_name", default="EvilTech CAD")
        environment = self._coerce_string(resolved_env.get("EVILTECH_ENV"), self._require_string(payload, "environment", default="development"))
        log_level = self._coerce_string(resolved_env.get("EVILTECH_LOG_LEVEL"), self._require_string(payload, "log_level", default="INFO"))
        workspace_root = self._optional_string(payload, "workspace_root")

        config = ApplicationConfiguration(
            app_name=app_name,
            environment=environment,
            log_level=log_level,
            workspace_root=workspace_root,
        )
        self._validate(config)
        return config

    def _validate(self, config: ApplicationConfiguration) -> None:
        """Validate a configuration object."""
        if not config.app_name or not config.app_name.strip():
            raise ConfigurationError("Configuration 'app_name' cannot be empty.")
        if not config.environment or not config.environment.strip():
            raise ConfigurationError("Configuration 'environment' cannot be empty.")
        if not config.log_level or not config.log_level.strip():
            raise ConfigurationError("Configuration 'log_level' cannot be empty.")

    @staticmethod
    def _require_string(payload: Mapping[str, Any], key: str, default: str | None = None) -> str:
        """Return a required string field from the payload."""
        value = payload.get(key, default)
        if value is None:
            raise ConfigurationError(f"Configuration '{key}' is required.")
        if not isinstance(value, str):
            raise ConfigurationError(f"Configuration '{key}' must be a string.")
        return value

    @staticmethod
    def _optional_string(payload: Mapping[str, Any], key: str) -> str | None:
        """Return an optional string field from the payload."""
        value = payload.get(key)
        if value is None:
            return None
        if not isinstance(value, str):
            raise ConfigurationError(f"Configuration '{key}' must be a string.")
        return value

    @staticmethod
    def _coerce_string(*values: str | None) -> str:
        """Choose the first non-empty string from a set of values."""
        for value in values:
            if value is not None and str(value).strip():
                return str(value)
        return ""
