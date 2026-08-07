"""General-purpose helper functions used across EvilTech CAD."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import Any, TypeVar

T = TypeVar("T")


def ensure_list(value: T | Iterable[T] | None) -> list[T]:
    """Return a value as a concrete list."""
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes, bytearray)):
        return list(value)
    return [value]


def flatten(items: Iterable[Iterable[T]]) -> list[T]:
    """Flatten a nested iterable one level deep."""
    return [item for group in items for item in group]


def deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    """Deep-merge mapping values without mutating the inputs."""
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, Mapping) and isinstance(merged.get(key), Mapping):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def slugify(value: str) -> str:
    """Convert a string into a filesystem-friendly slug."""
    text = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    return text.strip("-")


def compact_dict(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Remove keys with `None` values from a mapping."""
    return {key: value for key, value in payload.items() if value is not None}


def unique_by(items: Iterable[T], key: callable) -> list[T]:
    """Return items preserving order while removing duplicate keys."""
    seen: set[Any] = set()
    result: list[T] = []
    for item in items:
        marker = key(item)
        if marker in seen:
            continue
        seen.add(marker)
        result.append(item)
    return result
