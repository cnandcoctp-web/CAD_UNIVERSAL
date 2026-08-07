"""Manufacturability analysis for the AI pipeline."""

from __future__ import annotations

from AI.CONFIG.material_profiles import DEFAULT_MATERIAL_PROFILES
from AI.CONFIG.tolerances import AnalysisTolerances
from AI.SCHEMAS.analysis_schema import AnalysisFinding, DesignSnapshot
from AI.UTILS.calculations import clamp


class ManufacturabilityAnalyzer:
    """Estimate manufacturability using lightweight design heuristics."""

    def __init__(self, tolerances: AnalysisTolerances | None = None) -> None:
        self.tolerances = tolerances or AnalysisTolerances()

    def analyze(self, snapshot: DesignSnapshot) -> list[AnalysisFinding]:
        """Return manufacturability findings for a snapshot."""
        profile = DEFAULT_MATERIAL_PROFILES.get(snapshot.geometry.material_key, DEFAULT_MATERIAL_PROFILES["aluminum-6061"])
        complexity_penalty = min(0.6, len(snapshot.feature_names) * 0.02 + snapshot.geometry.total_faces() * 0.005)
        score = clamp(profile.machining_score - complexity_penalty)
        if score >= self.tolerances.low_manufacturability_score:
            return []
        return [AnalysisFinding("manufacturability", "critical", "Manufacturability score is low for the current feature and topology mix.", 0.79, {"score": score, "material": profile.key})]
