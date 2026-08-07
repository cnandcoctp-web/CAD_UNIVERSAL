"""Thread-safe queue for simulation jobs."""

from __future__ import annotations

from collections import deque
from threading import Lock


class SimulationQueue:
    """Thread-safe FIFO queue for simulation job identifiers."""

    def __init__(self) -> None:
        self._items: deque[str] = deque()
        self._lock = Lock()

    def enqueue(self, job_id: str) -> None:
        """Append a job identifier to the queue."""
        with self._lock:
            if job_id not in self._items:
                self._items.append(job_id)

    def dequeue(self) -> str | None:
        """Pop the next queued job identifier."""
        with self._lock:
            if not self._items:
                return None
            return self._items.popleft()

    def remove(self, job_id: str) -> bool:
        """Remove a queued job identifier if present."""
        with self._lock:
            try:
                self._items.remove(job_id)
            except ValueError:
                return False
            return True

    def is_empty(self) -> bool:
        """Return whether the queue is empty."""
        with self._lock:
            return not self._items

    def size(self) -> int:
        """Return the queue length."""
        with self._lock:
            return len(self._items)