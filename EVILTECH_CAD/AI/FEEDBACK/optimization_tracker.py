"""Optimization-tracking helpers for the AI pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class OptimizationTracker:
    """Track optimization opportunities surfaced by recommendations."""

    opportunities: list[str] = field(default_factory=list)

    def record(self, message: str) -> None:
        """Record an optimization opportunity."""
        self.opportunities.append(message)
