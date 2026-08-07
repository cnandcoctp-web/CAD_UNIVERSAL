"""Constraint analysis for the AI pipeline."""

from __future__ import annotations

from AI.SCHEMAS.analysis_schema import AnalysisFinding, DesignSnapshot


class ConstraintAnalyzer:
    """Detect risky constraint-system patterns."""

    def analyze(self, snapshot: DesignSnapshot) -> list[AnalysisFinding]:
        """Return findings related to constraint density."""
        count = int(snapshot.constraint_summary.get("constraint_count", 0))
        if count <= max(6, len(snapshot.feature_names) * 2):
            return []
        return [AnalysisFinding("constraints", "warning", "Constraint count is high relative to feature count.", 0.66, {"constraint_count": count})]
