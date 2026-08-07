"""Confidence aggregation for the AI pipeline."""

from __future__ import annotations

from AI.SCHEMAS.analysis_schema import AnalysisFinding
from AI.UTILS.calculations import weighted_average


class ConfidenceCalculator:
    """Aggregate confidence across findings and models."""

    def calculate(self, findings: list[AnalysisFinding]) -> float:
        """Return aggregate confidence for a set of findings."""
        if not findings:
            return 1.0
        pairs = [(finding.confidence, 1.0 if finding.severity == "critical" else 0.7) for finding in findings]
        return weighted_average(pairs)
