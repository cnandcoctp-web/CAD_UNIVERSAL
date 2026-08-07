"""Foundation engine for the EvilTech CAD platform.

The engine coordinates the core runtime services and exposes the foundation
state manager to the application shell. It is intentionally lightweight and
keeps the platform's runtime behavior explicit.
"""

from __future__ import annotations

from typing import Optional

from CORE.application_state_manager import ApplicationStateManager
from CORE.configuration import ApplicationConfiguration
from CORE.event_bus import EventBus
from CORE.logger import EvilTechLogger
from CORE.resource_manager import ResourceManager
from CORE.service_registry import ServiceRegistry


class FoundationEngine:
    """Coordinate the core runtime services for the application."""

    def __init__(self, config: ApplicationConfiguration) -> None:
        """Initialize the engine with its runtime dependencies."""
        self._config = config
        self._state_manager = ApplicationStateManager("ready")
        self._event_bus = EventBus()
        self._service_registry = ServiceRegistry()
        self._resource_manager = ResourceManager()
        self._logger = EvilTechLogger(name="eviltech.foundation", level=config.log_level)

    def start(self) -> None:
        """Start the engine and mark it ready for service use."""
        self._state_manager.set_state("ready")
        self._logger.info("Foundation engine started")

    def stop(self) -> None:
        """Stop the engine and transition it to the stopped state."""
        self._state_manager.set_state("stopped")
        self._logger.info("Foundation engine stopped")

    def get_state_manager(self) -> ApplicationStateManager:
        """Return the application state manager."""
        return self._state_manager

    def get_event_bus(self) -> EventBus:
        """Return the event bus used by foundation services."""
        return self._event_bus

    def get_service_registry(self) -> ServiceRegistry:
        """Return the service registry."""
        return self._service_registry

    def get_resource_manager(self) -> ResourceManager:
        """Return the resource manager."""
        return self._resource_manager

    def get_logger(self) -> EvilTechLogger:
        """Return the shared logger instance."""
        return self._logger
