"""Storage for AI processing performance history."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PerformanceHistory:
    """Track elapsed-time samples for AI processing."""

    samples: list[float] = field(default_factory=list)

    def record(self, elapsed_seconds: float) -> None:
        """Record a processing-duration sample."""
        self.samples.append(float(elapsed_seconds))

    def average(self) -> float:
        """Return the average processing duration."""
        return sum(self.samples) / len(self.samples) if self.samples else 0.0
