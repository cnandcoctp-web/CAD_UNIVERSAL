"""Deterministic AI controller for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass, field

from AI.ANALYSIS.analysis_registry import AnalysisRegistry
from AI.ANALYSIS.confidence_calculator import ConfidenceCalculator
from AI.ANALYSIS.design_analyzer import DesignAnalyzer
from AI.ANALYSIS.design_snapshot_builder import DesignSnapshotBuilder
from AI.ANALYSIS.geometry_state_classifier import GeometryStateClassifier
from AI.CONFIG.ai_settings import AISettings
from AI.DATA.data_registry import DataRegistry
from AI.DATA.data_validator import DataValidator
from AI.FEEDBACK.design_scorecard import DesignScorecard
from AI.FEEDBACK.feedback_registry import FeedbackRegistry
from AI.FEEDBACK.optimization_tracker import OptimizationTracker
from AI.FEEDBACK.performance_tracker import PerformanceTracker
from AI.MODELS.model_loader import ModelLoader
from AI.SCHEMAS.analysis_schema import AnalysisReport, DesignSnapshot
from AI.SCHEMAS.feedback_schema import FeedbackSummary
from AI.SCHEMAS.model_schema import ModelEvaluation
from AI.SCHEMAS.recommendation_schema import RecommendationBundle
from AI.SIGNALS.design_recommendation_generator import DesignRecommendationGenerator
from AI.SIGNALS.signal_registry import SignalRegistry
from AI.STORAGE.design_history import AIDesignHistory
from AI.STORAGE.model_metrics import ModelMetricsStore
from AI.STORAGE.performance_history import PerformanceHistory
from AI.STORAGE.recommendation_history import RecommendationHistory
from AI.STORAGE.state_cache import AIStateCache
from AI.UTILS.timer import ProcessingTimer
from AI.UTILS.validators import validate_snapshot


@dataclass(slots=True)
class AIProcessingResult:
    """End-to-end result of AI design processing."""

    report: AnalysisReport
    scorecard: DesignScorecard
    recommendations: RecommendationBundle
    geometry_state: str
    elapsed_seconds: float


@dataclass(slots=True)
class AIController:
    """Coordinate the deterministic AI analysis pipeline."""

    settings: AISettings = field(default_factory=AISettings)
    data_registry: DataRegistry = field(default_factory=DataRegistry)
    validator: DataValidator = field(default_factory=DataValidator)
    snapshot_builder: DesignSnapshotBuilder = field(default_factory=DesignSnapshotBuilder)
    analyses: AnalysisRegistry = field(default_factory=AnalysisRegistry)
    design_analyzer: DesignAnalyzer = field(default_factory=DesignAnalyzer)
    models: ModelLoader = field(default_factory=ModelLoader)
    signals: SignalRegistry = field(default_factory=SignalRegistry)
    confidence: ConfidenceCalculator = field(default_factory=ConfidenceCalculator)
    feedback_registry: FeedbackRegistry = field(default_factory=FeedbackRegistry)
    design_history: AIDesignHistory = field(default_factory=AIDesignHistory)
    recommendation_history: RecommendationHistory = field(default_factory=RecommendationHistory)
    performance_history: PerformanceHistory = field(default_factory=PerformanceHistory)
    model_metrics: ModelMetricsStore = field(default_factory=ModelMetricsStore)
    cache: AIStateCache = field(default_factory=AIStateCache)
    geometry_classifier: GeometryStateClassifier = field(default_factory=GeometryStateClassifier)
    optimization_tracker: OptimizationTracker = field(default_factory=OptimizationTracker)

    def process_part(self, part, constraints=None, material_key: str = "aluminum-6061") -> AIProcessingResult:
        """Process a part model through the AI pipeline."""
        timer = ProcessingTimer()
        geometry = self.data_registry.geometry.load_part(part, material_key=material_key)
        geometry_report = self.validator.validate_geometry(geometry)
        if not geometry_report.is_valid:
            raise ValueError("Invalid geometry dataset: " + "; ".join(geometry_report.errors))
        snapshot = self.snapshot_builder.build_part_snapshot(part, geometry, constraints)
        return self._process_snapshot(snapshot)

    def process_assembly(self, assembly, component_manager, material_key: str = "steel-1018") -> AIProcessingResult:
        """Process an assembly model through the AI pipeline."""
        geometry = self.data_registry.assemblies.load_assembly(assembly, component_manager, material_key=material_key)
        geometry_report = self.validator.validate_geometry(geometry)
        if not geometry_report.is_valid:
            raise ValueError("Invalid geometry dataset: " + "; ".join(geometry_report.errors))
        snapshot = self.snapshot_builder.build_assembly_snapshot(assembly, geometry)
        return self._process_snapshot(snapshot)

    def process_snapshot(self, snapshot: DesignSnapshot) -> AIProcessingResult:
        """Process a prebuilt snapshot through the AI pipeline."""
        return self._process_snapshot(snapshot)

    def _process_snapshot(self, snapshot: DesignSnapshot) -> AIProcessingResult:
        timer = ProcessingTimer()
        snapshot_report = validate_snapshot(snapshot)
        if not snapshot_report.is_valid:
            raise ValueError("Invalid design snapshot: " + "; ".join(snapshot_report.errors))

        findings = self.design_analyzer.analyze(snapshot, enabled=self.settings.enabled_analyses)
        aggregate_confidence = self.confidence.calculate(findings)
        report = AnalysisReport(snapshot=snapshot, findings=findings, confidence=aggregate_confidence, metrics={"entity_count": len(snapshot.geometry.entities)})

        registry = self.models.load()
        evaluations: list[ModelEvaluation] = [
            registry.geometry_model.evaluate(snapshot),
            registry.feature_model.evaluate(snapshot),
            registry.manufacturability_model.evaluate(snapshot),
            registry.constraint_model.evaluate(snapshot),
        ]
        for evaluation in evaluations:
            self.model_metrics.record(evaluation)
        quality = registry.quality_model.evaluate(evaluations)
        evaluations.append(quality)
        feedback_summary: FeedbackSummary = self.feedback_registry.summary()
        evaluations.append(registry.feedback_model.evaluate(feedback_summary))
        scorecard = DesignScorecard(evaluations=evaluations)

        generator = DesignRecommendationGenerator()
        recommendations = generator.generate(findings)
        recommendations = self.signals.confidence_filter.apply(recommendations, self.settings.minimum_confidence)
        recommendations = recommendations[: self.settings.max_recommendations]
        validation = self.signals.recommendation_validator.validate_many(recommendations)
        if not validation.is_valid:
            raise ValueError("Invalid recommendations: " + "; ".join(validation.errors))
        routes = self.signals.recommendation_router.route(recommendations)
        bundle = RecommendationBundle(recommendations=recommendations, routes=routes)

        for recommendation in recommendations:
            self.optimization_tracker.record(recommendation.description)
        self.recommendation_history.record_many(recommendations)
        self.design_history.record(snapshot)
        elapsed_seconds = timer.elapsed()
        PerformanceTracker().record(self.performance_history, elapsed_seconds)
        geometry_state = self.geometry_classifier.classify(snapshot)
        self.cache.set(snapshot.project_name, bundle)
        return AIProcessingResult(report=report, scorecard=scorecard, recommendations=bundle, geometry_state=geometry_state, elapsed_seconds=elapsed_seconds)
