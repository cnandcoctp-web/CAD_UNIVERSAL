"""Geometry scoring model for the AI pipeline."""

from __future__ import annotations

from AI.SCHEMAS.analysis_schema import DesignSnapshot
from AI.SCHEMAS.model_schema import ModelEvaluation
from AI.UTILS.calculations import clamp


class GeometryModel:
    """Score geometry complexity."""

    def evaluate(self, snapshot: DesignSnapshot) -> ModelEvaluation:
        """Return a geometry-complexity score."""
        score = clamp(1.0 - snapshot.geometry.total_faces() * 0.02)
        return ModelEvaluation("geometry_model", score=score, confidence=0.8, signals={"faces": snapshot.geometry.total_faces()})
