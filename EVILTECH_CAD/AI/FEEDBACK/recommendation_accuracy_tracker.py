"""Recommendation-accuracy tracking for the AI pipeline."""

from __future__ import annotations

from AI.FEEDBACK.feedback_registry import FeedbackRegistry


class RecommendationAccuracyTracker:
    """Compute coarse recommendation-acceptance metrics."""

    def accuracy(self, feedback_registry: FeedbackRegistry) -> float:
        """Return recommendation acceptance ratio."""
        summary = feedback_registry.summary()
        return summary.accepted / summary.total if summary.total else 1.0
