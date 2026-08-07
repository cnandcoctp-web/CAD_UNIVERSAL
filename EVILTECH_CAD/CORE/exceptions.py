"""Exception hierarchy for the EvilTech CAD foundation layer.

The exception classes provide a consistent and structured error model for the
foundation services. They are intentionally explicit so that higher-level
layers can distinguish configuration failures, runtime state problems,
and service registration issues.
"""

from __future__ import annotations


class EvilTechError(Exception):
    """Base exception for all EvilTech CAD foundation errors."""


class ConfigurationError(EvilTechError):
    """Raised when application configuration is invalid or incomplete."""


class EnvironmentError(EvilTechError):
    """Raised when environment resolution fails."""


class ProjectError(EvilTechError):
    """Raised when a project lifecycle operation fails."""


class SessionError(EvilTechError):
    """Raised when session management fails."""


class WorkspaceError(EvilTechError):
    """Raised when workspace initialization or activation fails."""


class ServiceRegistrationError(EvilTechError):
    """Raised when a service cannot be registered or resolved."""


class ResourceError(EvilTechError):
    """Raised when a resource cannot be registered or released correctly."""


class LoggingError(EvilTechError):
    """Raised when logging cannot be initialized or used."""


class EventBusError(EvilTechError):
    """Raised when event bus operations fail."""
