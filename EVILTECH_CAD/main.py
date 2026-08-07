"""Application entry point for the EvilTech CAD foundation layer.

This module provides the approved startup path for the foundation runtime.
It boots the application, initializes the core services, and shuts them down
cleanly after execution.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Sequence

from CORE.application import Application
from CORE.configuration import ApplicationConfiguration, ConfigurationLoader
from CORE.constants import APPLICATION_NAME, APPLICATION_VERSION
from CORE.exceptions import EvilTechError


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser for the application entry point."""
    parser = argparse.ArgumentParser(description="EvilTech CAD foundation launcher")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {APPLICATION_VERSION}",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Optional path to a JSON configuration file.",
    )
    parser.add_argument(
        "--environment",
        default=None,
        help="Optional runtime environment override.",
    )
    parser.add_argument(
        "--log-level",
        default=None,
        help="Optional log level override.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Bootstrap the EvilTech CAD foundation runtime.

    Args:
        argv: Optional command-line arguments.

    Returns:
        An exit code suitable for process-level execution.
    """
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    config: ApplicationConfiguration
    if args.config is not None:
        loader = ConfigurationLoader()
        env_mapping = {
            "EVILTECH_ENV": args.environment or os.environ.get("EVILTECH_ENV", "development"),
            "EVILTECH_LOG_LEVEL": args.log_level or os.environ.get("EVILTECH_LOG_LEVEL", "INFO"),
        }
        config = loader.load(args.config, env=env_mapping)
    else:
        config = ApplicationConfiguration(
            app_name=APPLICATION_NAME,
            environment=args.environment or os.environ.get("EVILTECH_ENV", "development"),
            log_level=args.log_level or os.environ.get("EVILTECH_LOG_LEVEL", "INFO"),
        )

    app = Application(config=config)
    started = False

    try:
        app.initialize_application(config)
        started = True
    except EvilTechError as exc:
        print(f"Failed to initialize EvilTech CAD: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Initialization interrupted by user.", file=sys.stderr)
        return 130

    try:
        app.shutdown_application()
    except EvilTechError as exc:
        print(f"Failed to shut down EvilTech CAD cleanly: {exc}", file=sys.stderr)
        return 1

    return 0 if started else 1


if __name__ == "__main__":
    raise SystemExit(main())
