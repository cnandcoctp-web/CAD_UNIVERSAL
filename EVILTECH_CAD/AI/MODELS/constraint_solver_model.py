"""Constraint-health scoring model for the AI pipeline."""

from __future__ import annotations

from AI.SCHEMAS.analysis_schema import DesignSnapshot
from AI.SCHEMAS.model_schema import ModelEvaluation
from AI.UTILS.calculations import clamp


class ConstraintSolverModel:
    """Score constraint-system health."""

    def evaluate(self, snapshot: DesignSnapshot) -> ModelEvaluation:
        """Return a constraint-system score."""
        count = float(snapshot.constraint_summary.get("constraint_count", 0))
        feature_count = max(1.0, float(len(snapshot.feature_names) or 1))
        score = clamp(1.0 - count / (feature_count * 6.0))
        return ModelEvaluation("constraint_solver_model", score=score, confidence=0.73, signals={"constraint_count": count})
