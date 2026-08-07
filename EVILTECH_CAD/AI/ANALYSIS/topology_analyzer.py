"""Topology analysis for the AI pipeline."""

from __future__ import annotations

from AI.CONFIG.tolerances import AnalysisTolerances
from AI.SCHEMAS.analysis_schema import AnalysisFinding, DesignSnapshot


class TopologyAnalyzer:
    """Detect geometry-complexity issues from topology metrics."""

    def __init__(self, tolerances: AnalysisTolerances | None = None) -> None:
        self.tolerances = tolerances or AnalysisTolerances()

    def analyze(self, snapshot: DesignSnapshot) -> list[AnalysisFinding]:
        """Return findings related to face and edge complexity."""
        face_count = snapshot.geometry.total_faces()
        if face_count < self.tolerances.high_complexity_faces:
            return []
        return [AnalysisFinding("geometry", "warning", "Topology is complex for the current design stage.", 0.68, {"face_count": face_count})]
