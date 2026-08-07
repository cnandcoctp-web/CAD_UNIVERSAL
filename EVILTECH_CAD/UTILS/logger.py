"""Structured logging helpers for EvilTech CAD."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class StructuredLogger:
    """Thin wrapper around the standard logging package."""

    name: str

    def __post_init__(self) -> None:
        self._logger = logging.getLogger(self.name)

    def log(self, level: int, message: str, **context: Any) -> None:
        """Log a message with flattened key-value context."""
        suffix = " ".join(f"{key}={value}" for key, value in sorted(context.items()))
        self._logger.log(level, f"{message}{' ' + suffix if suffix else ''}")

    def info(self, message: str, **context: Any) -> None:
        """Log an informational message."""
        self.log(logging.INFO, message, **context)

    def warning(self, message: str, **context: Any) -> None:
        """Log a warning message."""
        self.log(logging.WARNING, message, **context)

    def error(self, message: str, **context: Any) -> None:
        """Log an error message."""
        self.log(logging.ERROR, message, **context)
