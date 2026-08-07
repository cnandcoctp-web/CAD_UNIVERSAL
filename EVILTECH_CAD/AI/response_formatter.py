"""Response formatting for the AI Engineering Assistant."""

from __future__ import annotations

from AI.engineering_rule_engine import EngineeringRuleEngine
from AI.SCHEMAS.recommendation_schema import RecommendationBundle


class ResponseFormatter:
    """Format validated assistant responses for UI or API consumers."""

    def __init__(self, rule_engine: EngineeringRuleEngine | None = None) -> None:
        self.rule_engine = rule_engine or EngineeringRuleEngine()

    def format_assistant_response(
        self,
        discipline: str,
        report: dict[str, object],
        recommendations: RecommendationBundle,
        explanation: str,
    ) -> dict[str, object]:
        """Format and validate an assistant response payload."""
        response = {
            "discipline": discipline,
            "validated": True,
            "explanation": explanation,
            "recommendations": [recommendation.title for recommendation in recommendations.recommendations],
            "report_summary": report,
        }
        self.rule_engine.validate_response(response)
        return response