"""Design-history tracking for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class DesignHistoryEntry:
    """A single design-history event."""

    action: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=_utc_now)


class DesignHistoryTimeline:
    """Record and inspect design-history events."""

    def __init__(self) -> None:
        self._entries: list[DesignHistoryEntry] = []

    def record(self, action: str, **payload: Any) -> DesignHistoryEntry:
        """Append a new design-history event."""
        entry = DesignHistoryEntry(action=action, payload=dict(payload))
        self._entries.append(entry)
        return entry

    def entries(self) -> list[DesignHistoryEntry]:
        """Return history entries."""
        return list(self._entries)
