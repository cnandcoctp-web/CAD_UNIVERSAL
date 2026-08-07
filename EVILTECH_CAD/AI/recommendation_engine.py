"""Recommendation ranking for the AI Engineering Assistant."""

from __future__ import annotations

from AI.SCHEMAS.analysis_schema import AnalysisReport
from AI.SCHEMAS.recommendation_schema import Recommendation, RecommendationBundle


class RecommendationEngine:
    """Rank recommendations for presentation and optimization."""

    _priority_weight = {"high": 3, "medium": 2, "low": 1}

    def rank(self, report: AnalysisReport, bundle: RecommendationBundle) -> list[Recommendation]:
        """Return ranked recommendations using priority and confidence."""
        return sorted(
            bundle.recommendations,
            key=lambda item: (self._priority_weight.get(item.priority, 0), item.confidence, len(item.actions)),
            reverse=True,
        )