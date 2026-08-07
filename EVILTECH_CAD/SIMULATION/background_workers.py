"""Background worker coordination for simulation jobs."""

from __future__ import annotations

from concurrent.futures import Future
from typing import Any, Callable

from SIMULATION.multithreading_manager import MultiThreadingManager


class BackgroundWorkers:
    """Thin adapter over the shared simulation thread-pool manager."""

    def __init__(self, threading_manager: MultiThreadingManager) -> None:
        self.threading_manager = threading_manager

    def submit(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Future[Any]:
        """Submit background work."""
        return self.threading_manager.submit(func, *args, **kwargs)