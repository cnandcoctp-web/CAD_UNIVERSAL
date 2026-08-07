"""Thread-pool management for background simulation work."""

from __future__ import annotations

import atexit
from concurrent.futures import Future, ThreadPoolExecutor
from threading import Lock
from typing import Any, Callable


class MultiThreadingManager:
    """Manage the simulation framework thread pool."""

    def __init__(self, max_workers: int) -> None:
        if max_workers <= 0:
            raise ValueError("max_workers must be positive")
        self.max_workers = max_workers
        self._executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="simulation-worker")
        self._submitted = 0
        self._lock = Lock()
        self._shutdown = False
        atexit.register(self.shutdown)

    def submit(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Future[Any]:
        """Submit work to the thread pool."""
        with self._lock:
            self._submitted += 1
        return self._executor.submit(func, *args, **kwargs)

    def report(self) -> dict[str, int]:
        """Return simple thread-pool metrics."""
        with self._lock:
            return {"max_workers": self.max_workers, "submitted_tasks": self._submitted}

    def shutdown(self) -> None:
        """Shut down the thread pool."""
        with self._lock:
            if self._shutdown:
                return
            self._shutdown = True
        self._executor.shutdown(wait=True, cancel_futures=False)