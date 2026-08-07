"""In-memory caching utilities for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import monotonic
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class CacheEntry(Generic[T]):
    """A cache entry with an optional expiry timestamp."""

    value: T
    expires_at: float | None = None

    def expired(self) -> bool:
        """Return whether the entry has expired."""
        return self.expires_at is not None and monotonic() >= self.expires_at


class TTLCache(Generic[T]):
    """A simple TTL cache for deterministic local workflows."""

    def __init__(self) -> None:
        self._entries: dict[str, CacheEntry[T]] = {}

    def set(self, key: str, value: T, ttl_seconds: float | None = None) -> None:
        """Set a cached value with an optional TTL."""
        expiry = None if ttl_seconds is None else monotonic() + ttl_seconds
        self._entries[key] = CacheEntry(value=value, expires_at=expiry)

    def get(self, key: str, default: T | None = None) -> T | None:
        """Get a cached value if present and not expired."""
        entry = self._entries.get(key)
        if entry is None:
            return default
        if entry.expired():
            self._entries.pop(key, None)
            return default
        return entry.value

    def clear(self) -> None:
        """Clear all cached entries."""
        self._entries.clear()
