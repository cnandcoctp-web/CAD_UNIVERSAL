"""Validation for AI recommendations."""

from __future__ import annotations

from AI.SCHEMAS.recommendation_schema import Recommendation
from UTILS.validators import ValidationReport


class RecommendationValidator:
    """Validate outgoing recommendations."""

    def validate_many(self, recommendations: list[Recommendation]) -> ValidationReport:
        """Validate a recommendation batch."""
        report = ValidationReport()
        for recommendation in recommendations:
            if not recommendation.title:
                report.add_error("Recommendation title must be non-empty")
            if not recommendation.actions:
                report.add_error(f"Recommendation '{recommendation.identifier}' must have at least one action")
        return report
