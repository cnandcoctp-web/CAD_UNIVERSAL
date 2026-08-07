"""Serialization helpers for the AI pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from UTILS.serializer import dump_file, dumps, to_serializable


def export_payload(payload: Any, path: str | Path) -> Path:
    """Serialize an AI payload to disk."""
    return dump_file(payload, path)


__all__ = ["dumps", "export_payload", "to_serializable"]
