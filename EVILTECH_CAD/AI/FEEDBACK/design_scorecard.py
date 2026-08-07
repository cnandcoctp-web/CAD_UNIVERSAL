"""Scorecard helpers for the AI pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field

from AI.SCHEMAS.model_schema import ModelEvaluation


@dataclass(slots=True)
class DesignScorecard:
    """A summary of model scores for a processed design."""

    evaluations: list[ModelEvaluation] = field(default_factory=list)

    def overall_score(self) -> float:
        """Return the average score across evaluations."""
        return sum(item.score for item in self.evaluations) / len(self.evaluations) if self.evaluations else 0.0
