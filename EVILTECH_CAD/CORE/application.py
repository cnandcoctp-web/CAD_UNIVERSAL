"""Application bootstrap for the EvilTech CAD foundation layer.

The application class is the entry point for the approved foundation services.
It wires together configuration loading, environment resolution, service
registration, lifecycle management, and the foundation engine.
"""

from __future__ import annotations

from typing import Optional

from CORE.configuration import ApplicationConfiguration, ConfigurationLoader
from CORE.dependency_injection import DependencyInjector
from CORE.engine import FoundationEngine
from CORE.environment import EnvironmentManager
from CORE.event_bus import EventBus
from CORE.logger import EvilTechLogger
from CORE.plugin_discovery import PluginDiscoveryFramework
from CORE.project import ProjectLifecycleManager
from CORE.resource_manager import ResourceManager
from CORE.service_registry import ServiceRegistry
from CORE.session import SessionManager
from CORE.workspace import WorkspaceManager


class Application:
    """Bootstrap and coordinate the approved foundation services."""

    def __init__(self, config: Optional[ApplicationConfiguration] = None) -> None:
        """Initialize the application with optional configuration.

        Args:
            config: The application configuration. If omitted, a default
                configuration is used.
        """
        self.config = config or ApplicationConfiguration()
        self.environment_manager = EnvironmentManager()
        self.configuration_loader = ConfigurationLoader()
        self.logger = EvilTechLogger(name="eviltech.application", level=self.config.log_level)
        self.engine = FoundationEngine(self.config)
        self.dependency_injector = DependencyInjector()
        self.event_bus: EventBus = self.engine.get_event_bus()
        self.service_registry: ServiceRegistry = self.engine.get_service_registry()
        self.resource_manager: ResourceManager = self.engine.get_resource_manager()
        self.project_manager = ProjectLifecycleManager()
        self.session_manager = SessionManager()
        self.workspace_manager = WorkspaceManager()
        self.plugin_discovery = PluginDiscoveryFramework()

    def initialize_application(self, config: Optional[ApplicationConfiguration] = None) -> None:
        """Initialize the application runtime and its foundation services."""
        if config is not None:
            self.config = config
            self.logger = EvilTechLogger(name="eviltech.application", level=self.config.log_level)
        self.startup()

    def startup(self) -> None:
        """Start the application foundation services."""
        self.engine.start()
        self.service_registry.register("project_manager", self.project_manager)
        self.service_registry.register("session_manager", self.session_manager)
        self.service_registry.register("workspace_manager", self.workspace_manager)
        self.service_registry.register("event_bus", self.event_bus)
        self.service_registry.register("resource_manager", self.resource_manager)
        self.service_registry.register("plugin_discovery", self.plugin_discovery)
        self.service_registry.register("logger", self.logger)
        self.dependency_injector.register_singleton("application", self)
        self.dependency_injector.register_singleton("event_bus", self.event_bus)
        self.dependency_injector.register_singleton("service_registry", self.service_registry)
        self.dependency_injector.register_singleton("resource_manager", self.resource_manager)
        self.event_bus.publish("application.started", {"app_name": self.config.app_name})
        self.logger.info("Application startup completed")

    def shutdown(self) -> None:
        """Shut down the application foundation services."""
        self.event_bus.publish("application.stopped", {"app_name": self.config.app_name})
        self.engine.stop()
        self.logger.info("Application shutdown completed")

    def shutdown_application(self) -> None:
        """Shut down the application runtime and its foundation services."""
        self.shutdown()

    def load_configuration(self, path: str) -> ApplicationConfiguration:
        """Load configuration from a file and update application state."""
        loaded = self.configuration_loader.load(path, env=self.environment_manager._env)
        self.config = loaded
        self.environment_manager = EnvironmentManager(
            {**self.environment_manager._env, "EVILTECH_ENV": loaded.environment, "EVILTECH_LOG_LEVEL": loaded.log_level}
        )
        self.logger = EvilTechLogger(name="eviltech.application", level=self.config.log_level)
        return loaded


def main() -> None:
    """Entry point for the foundation application bootstrap."""
    Application().startup()
