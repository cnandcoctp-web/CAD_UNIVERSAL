"""Generic catalog infrastructure for EvilTech CAD data libraries."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class Catalog(Generic[T]):
    """A named in-memory catalog of reusable design data."""

    name: str
    entries: dict[str, T] = field(default_factory=dict)

    def register(self, key: str, value: T) -> None:
        """Register a value by key."""
        if not key or not key.strip():
            raise ValueError("key must be non-empty")
        self.entries[key] = value

    def get(self, key: str) -> T:
        """Return a value by key."""
        return self.entries[key]

    def list_keys(self) -> list[str]:
        """Return registered keys in sorted order."""
        return sorted(self.entries)


@dataclass(slots=True)
class LibraryBundle:
    """Aggregate project design-data catalogs."""

    materials: Catalog[object]
    fasteners: Catalog[object]
    bearings: Catalog[object]
    gears: Catalog[object]
    standards: Catalog[object]
    templates: Catalog[object]
    textures: Catalog[object]
    examples: Catalog[object]
