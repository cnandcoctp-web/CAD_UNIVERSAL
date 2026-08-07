"""Recommendation routing for the AI pipeline."""

from __future__ import annotations

from AI.CONFIG.recommendation_rules import RULE_TEMPLATES
from AI.SCHEMAS.recommendation_schema import Recommendation


class RecommendationRouter:
    """Assign recommendations to destination routes."""

    def route(self, recommendations: list[Recommendation]) -> dict[str, list[str]]:
        """Return route-to-recommendation-id mappings."""
        routes: dict[str, list[str]] = {}
        for recommendation in recommendations:
            route = recommendation.metadata.get("route") or RULE_TEMPLATES.get(recommendation.category, {}).get("route", "general")
            routes.setdefault(str(route), []).append(recommendation.identifier)
        return routes
