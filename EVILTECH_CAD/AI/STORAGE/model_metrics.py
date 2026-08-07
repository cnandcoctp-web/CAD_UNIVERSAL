"""Storage for AI model evaluation metrics."""

from __future__ import annotations

from dataclasses import dataclass, field

from AI.SCHEMAS.model_schema import ModelEvaluation


@dataclass(slots=True)
class ModelMetricsStore:
    """Collect model evaluations by model name."""

    evaluations: dict[str, list[ModelEvaluation]] = field(default_factory=dict)

    def record(self, evaluation: ModelEvaluation) -> None:
        """Record a model evaluation."""
        self.evaluations.setdefault(evaluation.model_name, []).append(evaluation)
