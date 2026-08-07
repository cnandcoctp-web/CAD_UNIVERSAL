"""Recommendation generation for the AI pipeline."""

from __future__ import annotations

from uuid import uuid4

from AI.CONFIG.constants import PRIORITIES
from AI.CONFIG.recommendation_rules import RULE_TEMPLATES
from AI.SCHEMAS.analysis_schema import AnalysisFinding
from AI.SCHEMAS.recommendation_schema import Recommendation


class DesignRecommendationGenerator:
    """Convert findings into actionable recommendations."""

    def generate(self, findings: list[AnalysisFinding]) -> list[Recommendation]:
        """Generate recommendations from analysis findings."""
        recommendations: list[Recommendation] = []
        for finding in findings:
            template = RULE_TEMPLATES.get(finding.category, {"title": finding.category.title(), "actions": ["Review the flagged design area"], "route": "general"})
            priority = "high" if finding.severity == "critical" else "medium"
            if priority not in PRIORITIES:
                priority = "low"
            recommendations.append(
                Recommendation(
                    identifier=str(uuid4()),
                    category=finding.category,
                    title=str(template["title"]),
                    description=finding.message,
                    priority=priority,
                    confidence=finding.confidence,
                    actions=list(template["actions"]),
                    metadata={"route": template["route"], **finding.details},
                )
            )
        return recommendations
