"""Performance-tracking helpers for the AI pipeline."""

from __future__ import annotations

from AI.STORAGE.performance_history import PerformanceHistory


class PerformanceTracker:
    """Record and report AI processing performance."""

    def record(self, history: PerformanceHistory, elapsed_seconds: float) -> float:
        """Store and return the updated average duration."""
        history.record(elapsed_seconds)
        return history.average()
