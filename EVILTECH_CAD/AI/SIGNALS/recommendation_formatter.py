"""Formatting helpers for AI recommendations."""

from __future__ import annotations

from AI.SCHEMAS.recommendation_schema import Recommendation


class RecommendationFormatter:
    """Format recommendations for presentation or export."""

    def format(self, recommendation: Recommendation) -> dict[str, object]:
        """Return a serializable presentation payload."""
        return {
            "id": recommendation.identifier,
            "title": recommendation.title,
            "category": recommendation.category,
            "priority": recommendation.priority,
            "confidence": round(recommendation.confidence, 3),
            "description": recommendation.description,
            "actions": list(recommendation.actions),
        }
