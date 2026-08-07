"""History tracking for simulation jobs."""

from __future__ import annotations

from threading import Lock
from typing import Any


class SimulationHistory:
    """Record state changes for simulation jobs."""

    def __init__(self) -> None:
        self._entries: dict[str, list[dict[str, Any]]] = {}
        self._lock = Lock()

    def record(self, job_id: str, status: str, **metadata: Any) -> None:
        """Record a job history event."""
        with self._lock:
            self._entries.setdefault(job_id, []).append({"status": status, **metadata})

    def entries(self, job_id: str) -> list[dict[str, Any]]:
        """Return recorded entries for a job."""
        with self._lock:
            return list(self._entries.get(job_id, []))