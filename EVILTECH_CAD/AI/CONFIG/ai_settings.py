"""Runtime settings for the deterministic AI pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field

from AI.CONFIG.tolerances import AnalysisTolerances


@dataclass(slots=True)
class AISettings:
    """User-configurable settings for AI processing."""

    enabled_analyses: list[str] = field(
        default_factory=lambda: ["geometry", "assembly", "features", "materials", "manufacturability", "constraints", "tolerances", "anomaly"]
    )
    max_recommendations: int = 10
    minimum_confidence: float = 0.5
    tolerances: AnalysisTolerances = field(default_factory=AnalysisTolerances)
