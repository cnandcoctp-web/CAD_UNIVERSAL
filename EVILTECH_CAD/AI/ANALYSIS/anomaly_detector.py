"""Anomaly detection for the AI pipeline."""

from __future__ import annotations

from AI.CONFIG.tolerances import AnalysisTolerances
from AI.SCHEMAS.analysis_schema import AnalysisFinding, DesignSnapshot


class AnomalyDetector:
    """Detect outlier geometry or feature counts."""

    def __init__(self, tolerances: AnalysisTolerances | None = None) -> None:
        self.tolerances = tolerances or AnalysisTolerances()

    def analyze(self, snapshot: DesignSnapshot) -> list[AnalysisFinding]:
        """Return anomaly findings."""
        entity_count = max(1, len(snapshot.geometry.entities))
        feature_factor = len(snapshot.feature_names) / entity_count
        if feature_factor <= self.tolerances.anomaly_feature_factor:
            return []
        return [AnalysisFinding("anomaly", "warning", "Feature density is unusually high for the number of entities.", 0.74, {"feature_factor": feature_factor})]
