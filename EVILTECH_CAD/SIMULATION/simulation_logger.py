"""Structured logging for simulation jobs."""

from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock
from typing import Any


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class SimulationLogger:
    """Collect structured job log entries."""

    def __init__(self) -> None:
        self._entries: dict[str, list[dict[str, Any]]] = {}
        self._lock = Lock()

    def log(self, job_id: str, event: str, message: str, **metadata: Any) -> None:
        """Append a job log entry."""
        payload = {"timestamp": _utc_now(), "event": event, "message": message, **metadata}
        with self._lock:
            self._entries.setdefault(job_id, []).append(payload)

    def entries(self, job_id: str) -> list[dict[str, Any]]:
        """Return log entries for a job."""
        with self._lock:
            return list(self._entries.get(job_id, []))