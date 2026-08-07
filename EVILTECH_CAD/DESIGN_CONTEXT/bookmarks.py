"""Bookmark management for EvilTech CAD design context."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class Bookmark:
    """A bookmark to a saved design view or selection."""

    name: str
    payload: dict[str, object] = field(default_factory=dict)
    created_at: str = field(default_factory=_utc_now)


class BookmarkManager:
    """Store and retrieve design bookmarks."""

    def __init__(self) -> None:
        self._bookmarks: dict[str, Bookmark] = {}

    def save(self, bookmark: Bookmark) -> None:
        """Save or replace a bookmark."""
        self._bookmarks[bookmark.name] = bookmark

    def get(self, name: str) -> Bookmark:
        """Return a bookmark by name."""
        return self._bookmarks[name]

    def list_names(self) -> list[str]:
        """Return bookmark names in sorted order."""
        return sorted(self._bookmarks)
