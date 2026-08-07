"""Feedback-learning heuristics for the AI pipeline."""

from __future__ import annotations

from AI.SCHEMAS.feedback_schema import FeedbackSummary
from AI.SCHEMAS.model_schema import ModelEvaluation
from AI.UTILS.calculations import clamp


class FeedbackLearningModel:
    """Derive a trust score from historical feedback."""

    def evaluate(self, feedback: FeedbackSummary) -> ModelEvaluation:
        """Return a feedback-based trust score."""
        acceptance_ratio = feedback.accepted / feedback.total if feedback.total else 1.0
        score = clamp((acceptance_ratio + feedback.average_rating / 5.0) / 2.0)
        return ModelEvaluation("feedback_learning_model", score=score, confidence=0.65, signals={"total_feedback": feedback.total})
