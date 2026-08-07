"""Material analyzer for the AI Engineering Assistant."""

from __future__ import annotations

from AI.CONFIG.material_profiles import DEFAULT_MATERIAL_PROFILES
from AI.SCHEMAS.analysis_schema import AnalysisFinding, DesignSnapshot


class MaterialAnalyzer:
    """Analyze material suitability for the reviewed design."""

    def analyze(self, snapshot: DesignSnapshot) -> list[AnalysisFinding]:
        """Return material-related findings."""
        profile = DEFAULT_MATERIAL_PROFILES.get(snapshot.geometry.material_key)
        if profile is None:
            return [AnalysisFinding("materials", "warning", "No AI material profile is registered for the selected material.", 0.63, {"material": snapshot.geometry.material_key})]
        if profile.machining_score >= 0.5:
            return []
        return [AnalysisFinding("materials", "warning", "Selected material may raise manufacturing cost or process difficulty.", 0.71, {"material": profile.key})]