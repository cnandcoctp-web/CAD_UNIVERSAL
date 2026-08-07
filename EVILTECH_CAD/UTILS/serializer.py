"""Serialization helpers for EvilTech CAD."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any


def to_serializable(value: Any) -> Any:
    """Convert common project objects into JSON-serializable data."""
    if is_dataclass(value):
        return {key: to_serializable(item) for key, item in asdict(value).items()}
    if hasattr(value, "to_dict"):
        return to_serializable(value.to_dict())
    if isinstance(value, dict):
        return {str(key): to_serializable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_serializable(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value


def dumps(value: Any, *, indent: int = 2) -> str:
    """Serialize a value to formatted JSON text."""
    return json.dumps(to_serializable(value), indent=indent, sort_keys=True)


def dump_file(value: Any, path: str | Path) -> Path:
    """Serialize a value to a JSON file."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dumps(value), encoding="utf-8")
    return target


def loads(value: str) -> Any:
    """Deserialize JSON text."""
    return json.loads(value)
