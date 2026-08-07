"""Optimization planning for the AI Engineering Assistant."""

from __future__ import annotations

from AI.SCHEMAS.analysis_schema import AnalysisReport
from AI.SCHEMAS.recommendation_schema import Recommendation


class OptimizationEngine:
    """Convert recommendations into a coarse optimization plan."""

    def build_plan(self, report: AnalysisReport, recommendations: list[Recommendation]) -> dict[str, object]:
        """Build a lightweight optimization plan from ranked recommendations."""
        opportunities = [recommendation.title for recommendation in recommendations[:5]]
        estimated_impact = min(1.0, sum(recommendation.confidence for recommendation in recommendations[:3]) / 3.0) if recommendations else 0.0
        return {
            "project_name": report.snapshot.project_name,
            "opportunities": opportunities,
            "estimated_impact": estimated_impact,
            "focus_areas": sorted({recommendation.category for recommendation in recommendations}),
        }