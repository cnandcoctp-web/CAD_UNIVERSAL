"""Tolerance analysis for the AI pipeline."""

from __future__ import annotations

from AI.SCHEMAS.analysis_schema import AnalysisFinding, DesignSnapshot


class ToleranceAnalyzer:
    """Detect tolerance strategies likely to be over-constrained."""

    def analyze(self, snapshot: DesignSnapshot) -> list[AnalysisFinding]:
        """Return findings related to tolerance metadata."""
        tolerances = snapshot.metadata.get("tolerances")
        if not isinstance(tolerances, dict):
            return []
        minimum = float(tolerances.get("minimum", 0.0))
        if minimum >= 0.01:
            return []
        return [AnalysisFinding("tolerances", "warning", "Very tight tolerances detected for early design stages.", 0.7, {"minimum": minimum})]
