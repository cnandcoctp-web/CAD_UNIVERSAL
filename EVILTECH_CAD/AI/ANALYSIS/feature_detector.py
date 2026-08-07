"""Feature-pattern analysis for the AI pipeline."""

from __future__ import annotations

from AI.SCHEMAS.analysis_schema import AnalysisFinding, DesignSnapshot


class FeatureDetector:
    """Detect feature-stack complexity patterns."""

    def analyze(self, snapshot: DesignSnapshot) -> list[AnalysisFinding]:
        """Return findings related to feature count and layering."""
        findings: list[AnalysisFinding] = []
        feature_count = len(snapshot.feature_names)
        if feature_count >= 12:
            findings.append(AnalysisFinding("features", "warning", "Feature stack is becoming complex.", 0.72, {"feature_count": feature_count}))
        if feature_count >= 20:
            findings.append(AnalysisFinding("features", "critical", "Feature stack may be difficult to maintain and regenerate.", 0.83, {"feature_count": feature_count}))
        return findings
