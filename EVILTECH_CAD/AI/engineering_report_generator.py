"""Engineering report generation for the AI Engineering Assistant."""

from __future__ import annotations

from AI.FEEDBACK.design_scorecard import DesignScorecard
from AI.SCHEMAS.analysis_schema import AnalysisReport
from AI.SCHEMAS.recommendation_schema import RecommendationBundle


class EngineeringReportGenerator:
    """Generate structured engineering reports from AI outputs."""

    def generate(
        self,
        report: AnalysisReport,
        scorecard: DesignScorecard,
        recommendations: RecommendationBundle,
        discipline: str,
        project_id: str | None = None,
    ) -> dict[str, object]:
        """Create a deterministic engineering report payload."""
        return {
            "project_id": project_id,
            "project_name": report.snapshot.project_name,
            "discipline": discipline,
            "finding_count": report.finding_count(),
            "recommendation_count": len(recommendations.recommendations),
            "overall_score": scorecard.overall_score(),
            "confidence": report.confidence,
            "metrics": dict(report.metrics),
        }