"""Timing helpers for the AI pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter


@dataclass(slots=True)
class ProcessingTimer:
    """Measure elapsed AI processing time."""

    started_at: float = field(default_factory=perf_counter)

    def elapsed(self) -> float:
        """Return elapsed time in seconds."""
        return perf_counter() - self.started_at
