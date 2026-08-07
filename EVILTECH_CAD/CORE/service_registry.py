"""Service registry for the EvilTech CAD foundation layer.

The registry provides a safe and explicit mechanism for registering runtime
services that are resolved by name. This keeps the foundation services loosely
coupled and supports later dependency injection.
"""

from __future__ import annotations

from typing import Any, Dict, List

from CORE.exceptions import ServiceRegistrationError


class ServiceRegistry:
    """Register and resolve named services."""

    def __init__(self) -> None:
        """Initialize the registry."""
        self._services: Dict[str, Any] = {}

    def register(self, name: str, service: Any, override: bool = False) -> None:
        """Register a service under a unique name.

        Args:
            name: The service name.
            service: The service implementation.
            override: Whether an existing registration may be replaced.

        Raises:
            ServiceRegistrationError: If a duplicate registration is attempted
                without explicit override.
        """
        if not name or not name.strip():
            raise ServiceRegistrationError("Service names must be non-empty.")
        if name in self._services and not override:
            raise ServiceRegistrationError(f"Service '{name}' is already registered.")
        self._services[name] = service

    def resolve(self, name: str) -> Any:
        """Resolve a service by name.

        Args:
            name: The service name.

        Returns:
            The registered service.

        Raises:
            ServiceRegistrationError: If the service is not registered.
        """
        if name not in self._services:
            raise ServiceRegistrationError(f"Service '{name}' is not registered.")
        return self._services[name]

    def has_service(self, name: str) -> bool:
        """Return whether a service is registered."""
        return name in self._services

    def list_services(self) -> List[str]:
        """Return the registered service names."""
        return sorted(self._services.keys())
