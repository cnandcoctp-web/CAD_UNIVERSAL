"""Overall design-quality model for the AI pipeline."""

from __future__ import annotations

from AI.SCHEMAS.model_schema import ModelEvaluation
from AI.UTILS.calculations import weighted_average


class DesignQualityModel:
    """Combine model outputs into an overall quality score."""

    def evaluate(self, evaluations: list[ModelEvaluation]) -> ModelEvaluation:
        """Return an aggregated design-quality score."""
        score = weighted_average([(evaluation.score, evaluation.confidence) for evaluation in evaluations]) if evaluations else 1.0
        confidence = weighted_average([(evaluation.confidence, 1.0) for evaluation in evaluations]) if evaluations else 1.0
        return ModelEvaluation("design_quality_model", score=score, confidence=confidence, signals={"model_count": len(evaluations)})
