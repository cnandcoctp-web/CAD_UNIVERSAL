"""Storage for generated recommendations."""

from __future__ import annotations

from dataclasses import dataclass, field

from AI.SCHEMAS.recommendation_schema import Recommendation


@dataclass(slots=True)
class RecommendationHistory:
    """Store emitted recommendations across runs."""

    items: list[Recommendation] = field(default_factory=list)

    def record_many(self, recommendations: list[Recommendation]) -> None:
        """Append a batch of recommendations."""
        self.items.extend(recommendations)
