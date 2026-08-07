"""Dependency injection support for the EvilTech CAD foundation layer.

The container provides a simple, explicit, and defensive mechanism for
registering singleton services and factory functions. It is intentionally
lightweight so that later phases can build on it without introducing a heavy
framework dependency.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Generic, TypeVar

from CORE.exceptions import ServiceRegistrationError

T = TypeVar("T")


class DependencyInjector:
    """A minimal dependency injection container for foundation services."""

    def __init__(self) -> None:
        """Initialize an empty dependency container."""
        self._singletons: Dict[str, Any] = {}
        self._factories: Dict[str, Callable[[], Any]] = {}

    def register_singleton(self, name: str, instance: Any, override: bool = False) -> None:
        """Register a singleton instance for a named dependency.

        Args:
            name: The dependency name.
            instance: The instance to expose.
            override: Whether an existing registration may be replaced.

        Raises:
            ServiceRegistrationError: If the dependency name is invalid or
                already registered without override.
        """
        if not name or not name.strip():
            raise ServiceRegistrationError("Dependency name must be non-empty.")
        if name in self._singletons and not override:
            raise ServiceRegistrationError(f"Dependency '{name}' is already registered.")
        self._singletons[name] = instance

    def register_factory(self, name: str, factory: Callable[[], Any], override: bool = False) -> None:
        """Register a factory function for a named dependency.

        Args:
            name: The dependency name.
            factory: A callable that creates the dependency.
            override: Whether an existing registration may be replaced.

        Raises:
            ServiceRegistrationError: If the dependency name is invalid or
                already registered without override.
        """
        if not name or not name.strip():
            raise ServiceRegistrationError("Dependency name must be non-empty.")
        if name in self._factories and not override:
            raise ServiceRegistrationError(f"Dependency '{name}' is already registered.")
        if not callable(factory):
            raise ServiceRegistrationError("Dependency factory must be callable.")
        self._factories[name] = factory

    def resolve(self, name: str) -> Any:
        """Resolve a dependency by name.

        Args:
            name: The dependency name.

        Returns:
            The resolved dependency.

        Raises:
            ServiceRegistrationError: If the dependency is not registered.
        """
        if name in self._singletons:
            return self._singletons[name]
        if name in self._factories:
            instance = self._factories[name]()
            self._singletons[name] = instance
            return instance
        raise ServiceRegistrationError(f"Dependency '{name}' is not registered.")
