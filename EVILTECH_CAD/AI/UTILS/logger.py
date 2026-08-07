"""Logging helpers for the AI pipeline."""

from __future__ import annotations

from UTILS.logger import StructuredLogger


def get_ai_logger(name: str = "eviltech.ai") -> StructuredLogger:
    """Return a structured logger for the AI package."""
    return StructuredLogger(name)
