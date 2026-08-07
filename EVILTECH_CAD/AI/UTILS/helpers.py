"""Small helper functions for the AI pipeline."""

from __future__ import annotations

from typing import Iterable, TypeVar

T = TypeVar("T")


def top_n(items: Iterable[T], count: int, key) -> list[T]:
    """Return the top `count` items ordered by the supplied key."""
    return sorted(items, key=key, reverse=True)[:count]


def histogram(values: Iterable[str]) -> dict[str, int]:
    """Return a frequency mapping for string values."""
    result: dict[str, int] = {}
    for value in values:
        result[value] = result.get(value, 0) + 1
    return result
