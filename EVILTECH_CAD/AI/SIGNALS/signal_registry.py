"""Registry of signal-processing helpers for the AI pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field

from AI.SIGNALS.confidence_filter import ConfidenceFilter
from AI.SIGNALS.manufacturability_classifier import ManufacturabilityClassifier
from AI.SIGNALS.recommendation_exporter import RecommendationExporter
from AI.SIGNALS.recommendation_formatter import RecommendationFormatter
from AI.SIGNALS.recommendation_router import RecommendationRouter
from AI.SIGNALS.recommendation_validator import RecommendationValidator


@dataclass(slots=True)
class SignalRegistry:
    """Bundle signal-processing helpers."""

    confidence_filter: ConfidenceFilter = field(default_factory=ConfidenceFilter)
    manufacturability_classifier: ManufacturabilityClassifier = field(default_factory=ManufacturabilityClassifier)
    recommendation_exporter: RecommendationExporter = field(default_factory=RecommendationExporter)
    recommendation_formatter: RecommendationFormatter = field(default_factory=RecommendationFormatter)
    recommendation_router: RecommendationRouter = field(default_factory=RecommendationRouter)
    recommendation_validator: RecommendationValidator = field(default_factory=RecommendationValidator)
