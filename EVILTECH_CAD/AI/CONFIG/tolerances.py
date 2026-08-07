"""AI scoring and analysis tolerances."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AnalysisTolerances:
    """Thresholds for deterministic AI analysis heuristics."""

    low_confidence: float = 0.45
    high_complexity_faces: int = 24
    low_manufacturability_score: float = 0.45
    anomaly_feature_factor: float = 2.5
