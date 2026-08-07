"""Manufacturability scoring model for the AI pipeline."""

from __future__ import annotations

from AI.CONFIG.material_profiles import DEFAULT_MATERIAL_PROFILES
from AI.SCHEMAS.analysis_schema import DesignSnapshot
from AI.SCHEMAS.model_schema import ModelEvaluation
from AI.UTILS.calculations import clamp


class ManufacturabilityModel:
    """Score likely manufacturability from material and complexity."""

    def evaluate(self, snapshot: DesignSnapshot) -> ModelEvaluation:
        """Return a manufacturability score."""
        profile = DEFAULT_MATERIAL_PROFILES.get(snapshot.geometry.material_key, DEFAULT_MATERIAL_PROFILES["aluminum-6061"])
        score = clamp(profile.machining_score - len(snapshot.feature_names) * 0.025 - snapshot.geometry.total_faces() * 0.004)
        return ModelEvaluation("manufacturability_model", score=score, confidence=0.82, signals={"material": profile.key})
