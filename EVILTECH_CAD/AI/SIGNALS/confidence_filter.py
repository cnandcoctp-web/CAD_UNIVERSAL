"""Confidence filtering for recommendations."""

from __future__ import annotations

from AI.SCHEMAS.recommendation_schema import Recommendation


class ConfidenceFilter:
    """Filter recommendations below a minimum confidence."""

    def apply(self, recommendations: list[Recommendation], minimum_confidence: float) -> list[Recommendation]:
        """Return recommendations meeting the confidence threshold."""
        return [recommendation for recommendation in recommendations if recommendation.confidence >= minimum_confidence]
