"""Resource lifecycle management for the EvilTech CAD foundation layer.

The resource manager tracks shared runtime resources such as buffers,
configuration objects, and other objects that must be registered and released
explicitly. It is intentionally simple and defensive.
"""

from __future__ import annotations

from typing import Any, Dict, List

from CORE.exceptions import ResourceError


class ResourceManager:
    """Manage named runtime resources with explicit registration and release."""

    def __init__(self) -> None:
        """Initialize the resource manager."""
        self._resources: Dict[str, Any] = {}

    def register_resource(self, name: str, resource: Any) -> None:
        """Register a resource under a unique name.

        Args:
            name: The resource name.
            resource: The resource object to register.

        Raises:
            ResourceError: If the name is empty or already registered.
        """
        if not name or not name.strip():
            raise ResourceError("Resource names must be non-empty.")
        if name in self._resources:
            raise ResourceError(f"Resource '{name}' is already registered.")
        self._resources[name] = resource

    def get_resource(self, name: str) -> Any:
        """Return the resource registered under ``name``.

        Args:
            name: The resource name.

        Returns:
            The registered resource.

        Raises:
            ResourceError: If the resource does not exist.
        """
        if name not in self._resources:
            raise ResourceError(f"Resource '{name}' is not registered.")
        return self._resources[name]

    def release_resource(self, name: str) -> None:
        """Release a resource if it exists.

        Args:
            name: The resource name.
        """
        self._resources.pop(name, None)

    def list_resources(self) -> List[str]:
        """Return the currently registered resource names."""
        return sorted(self._resources.keys())
