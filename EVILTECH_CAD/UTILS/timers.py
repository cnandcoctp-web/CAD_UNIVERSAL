"""Timing utilities for lightweight profiling."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter


@dataclass(slots=True)
class Stopwatch:
    """A simple stopwatch for measuring elapsed durations."""

    _started_at: float = field(default_factory=perf_counter)

    def restart(self) -> None:
        """Restart the stopwatch."""
        self._started_at = perf_counter()

    def elapsed(self) -> float:
        """Return the elapsed time in seconds."""
        return perf_counter() - self._started_at
