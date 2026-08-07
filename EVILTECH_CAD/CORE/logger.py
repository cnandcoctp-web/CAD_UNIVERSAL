"""Logging infrastructure for the EvilTech CAD foundation layer.

The logger wrapper provides a consistent application logger that can be used
across services and that integrates defensive logging behavior with the
approved configuration model.
"""

from __future__ import annotations

import logging
from typing import Optional

from CORE.exceptions import LoggingError


class EvilTechLogger:
    """A defensive logging wrapper over Python's standard logging module."""

    def __init__(self, name: str, level: str = "INFO") -> None:
        """Initialize the logger wrapper.

        Args:
            name: The logger name.
            level: The minimum logging level to emit.

        Raises:
            LoggingError: If the logger name or level is invalid.
        """
        if not name or not name.strip():
            raise LoggingError("Logger name must be non-empty.")
        self._name = name
        self._level = self._normalize_level(level)
        self._logger = logging.getLogger(name)
        self._logger.setLevel(self._level)
        self._logger.propagate = False
        self._logger.handlers.clear()
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
        self._logger.addHandler(handler)

    def get_logger(self) -> logging.Logger:
        """Return the underlying logger instance."""
        return self._logger

    def debug(self, message: str, *args: object) -> None:
        """Emit a debug log entry."""
        self._logger.debug(message, *args)

    def info(self, message: str, *args: object) -> None:
        """Emit an info log entry."""
        self._logger.info(message, *args)

    def warning(self, message: str, *args: object) -> None:
        """Emit a warning log entry."""
        self._logger.warning(message, *args)

    def error(self, message: str, *args: object) -> None:
        """Emit an error log entry."""
        self._logger.error(message, *args)

    @staticmethod
    def _normalize_level(level: str) -> int:
        """Normalize a string level to a logging constant."""
        normalized = (level or "INFO").upper()
        try:
            return getattr(logging, normalized)
        except AttributeError as exc:
            raise LoggingError(f"Unsupported log level: {level}") from exc
