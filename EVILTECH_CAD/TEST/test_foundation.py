"""Tests for the approved EvilTech CAD foundation layer."""

# pyright: reportMissingImports=false

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from CORE.application import Application
from CORE.application_state_manager import ApplicationStateManager
from main import main
from CORE.configuration import ApplicationConfiguration, ConfigurationLoader
from CORE.environment import EnvironmentManager
from CORE.event_bus import EventBus, EventEnvelope
from CORE.exceptions import ConfigurationError, ProjectError, ServiceRegistrationError
from CORE.logger import EvilTechLogger
from CORE.plugin_discovery import PluginDiscoveryFramework
from CORE.project import ProjectLifecycleManager
from CORE.resource_manager import ResourceManager
from CORE.service_registry import ServiceRegistry
from CORE.session import SessionManager
from CORE.workspace import WorkspaceManager


def test_configuration_loader_loads_json_and_environment(tmp_path: Path) -> None:
    """Configuration loading should parse configuration files and environment overrides."""
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"app_name": "TestApp", "environment": "testing"}), encoding="utf-8")

    loader = ConfigurationLoader()
    config = loader.load(config_path, env={"EVILTECH_LOG_LEVEL": "DEBUG", "EVILTECH_ENV": "production"})

    assert config.app_name == "TestApp"
    assert config.environment == "production"
    assert config.log_level == "DEBUG"


def test_configuration_loader_rejects_invalid_configuration() -> None:
    """Invalid configuration data should raise a configuration error."""
    loader = ConfigurationLoader()
    with pytest.raises(ConfigurationError):
        loader.load_from_mapping({"app_name": "", "environment": ""})


def test_event_bus_delivers_subscribed_events() -> None:
    """The event bus should publish payloads to all subscribers."""
    bus = EventBus()
    received: list[EventEnvelope] = []

    bus.subscribe("sample", lambda event: received.append(event))
    bus.publish("sample", {"value": 1})

    assert len(received) == 1
    assert received[0].payload["value"] == 1


def test_logger_is_configurable_and_returns_logger() -> None:
    """The application logger should expose a usable logger instance."""
    logger = EvilTechLogger("test-logger", level="DEBUG")
    assert logger.get_logger().name == "test-logger"


def test_logger_does_not_propagate_to_root_handlers() -> None:
    """The logger should isolate itself from root logging propagation."""
    logger = EvilTechLogger("isolated-logger", level="INFO")
    assert logger.get_logger().propagate is False


def test_project_lifecycle_manager_creates_opens_and_closes_projects() -> None:
    """Projects should move through lifecycle states correctly."""
    manager = ProjectLifecycleManager()
    project = manager.create_project(name="Demo Project")

    assert project.name == "Demo Project"
    assert project.lifecycle_state.value == "created"

    reopened = manager.open_project(project.id)
    assert reopened.lifecycle_state.value == "opened"

    closed = manager.close_project(project.id)
    assert closed.lifecycle_state.value == "closed"


def test_project_lifecycle_manager_rejects_missing_project() -> None:
    """Missing projects should be reported with a project error."""
    manager = ProjectLifecycleManager()
    with pytest.raises(ProjectError):
        manager.open_project("does-not-exist")


def test_session_manager_creates_and_closes_sessions() -> None:
    """Sessions should be created and closed through the session manager."""
    manager = SessionManager()
    session = manager.create_session("demo")
    assert session.state.value == "active"

    closed = manager.close_session(session.id)
    assert closed.state.value == "closed"


def test_workspace_manager_initializes_and_activates_workspaces() -> None:
    """Workspace initialization and activation should be explicit and stateful."""
    manager = WorkspaceManager()
    workspace = manager.create_workspace("test-workspace", "default")
    initialized = manager.initialize_workspace(workspace.id)
    activated = manager.activate_workspace(initialized.id)

    assert initialized.state.value == "initialized"
    assert activated.state.value == "active"


def test_service_registry_registers_and_resolves_services() -> None:
    """Services should be registered and resolved through the registry."""
    registry = ServiceRegistry()
    registry.register("demo", {"value": 1})

    resolved = registry.resolve("demo")
    assert resolved["value"] == 1


def test_service_registry_rejects_duplicate_registration_without_override() -> None:
    """Duplicate registration should be rejected unless explicitly overridden."""
    registry = ServiceRegistry()
    registry.register("demo", {"value": 1})
    with pytest.raises(ServiceRegistrationError):
        registry.register("demo", {"value": 2})


def test_application_state_manager_tracks_state_changes() -> None:
    """Application state should be trackable and observable."""
    manager = ApplicationStateManager()
    manager.set_state("ready")
    snapshot = manager.snapshot()

    assert snapshot["state"] == "ready"


def test_resource_manager_registers_and_releases_resources() -> None:
    """Resources should be registered, retrieved, and released cleanly."""
    manager = ResourceManager()
    manager.register_resource("demo", {"value": 1})

    assert manager.get_resource("demo")["value"] == 1

    manager.release_resource("demo")
    assert "demo" not in manager.list_resources()


def test_plugin_discovery_finds_manifests() -> None:
    """Plugin discovery should find plugin manifests on disk."""
    framework = PluginDiscoveryFramework()
    manifests = framework.discover_plugins([Path(__file__).resolve().parent])
    assert isinstance(manifests, list)


def test_environment_manager_resolves_environment_values() -> None:
    """Environment values should resolve from the provided environment mapping."""
    manager = EnvironmentManager({"EVILTECH_ENV": "test"})
    assert manager.get_environment() == "test"


def test_application_load_configuration_updates_environment_manager(tmp_path: Path) -> None:
    """Loading configuration should update the runtime environment view."""
    app = Application(config=ApplicationConfiguration(app_name="FoundationTest", environment="testing"))
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"app_name": "LoadedApp", "environment": "production"}), encoding="utf-8")

    loaded = app.load_configuration(str(config_path))

    assert loaded.environment == "production"
    assert app.environment_manager.get_environment(default="development") == "production"


def test_application_bootstrap_and_shutdown_are_coordinated() -> None:
    """The application should bootstrap and shut down the foundation services."""
    app = Application(config=ApplicationConfiguration(app_name="FoundationTest", environment="testing"))
    app.startup()

    assert app.engine is not None
    assert app.engine.get_state_manager().get_state().value == "ready"

    app.shutdown()
    assert app.engine.get_state_manager().get_state().value == "stopped"


def test_main_entrypoint_bootstraps_and_shutdowns_cleanly() -> None:
    """The application entry point should start and stop the foundation services cleanly."""
    exit_code = main([])

    assert exit_code == 0
