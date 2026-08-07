"""Recommendation export helpers."""

from __future__ import annotations

from pathlib import Path

from AI.SIGNALS.recommendation_formatter import RecommendationFormatter
from AI.SCHEMAS.recommendation_schema import RecommendationBundle
from AI.UTILS.serializer import export_payload


class RecommendationExporter:
    """Export formatted recommendation bundles."""

    def export(self, bundle: RecommendationBundle, path: str | Path) -> Path:
        """Write formatted recommendations to disk."""
        formatter = RecommendationFormatter()
        payload = {
            "recommendations": [formatter.format(recommendation) for recommendation in bundle.recommendations],
            "routes": dict(bundle.routes),
        }
        return export_payload(payload, path)
