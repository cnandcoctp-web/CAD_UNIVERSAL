"""Registry of AI analyzers."""

from __future__ import annotations

from dataclasses import dataclass, field

from AI.ANALYSIS.anomaly_detector import AnomalyDetector
from AI.ANALYSIS.assembly_analyzer import AssemblyAnalyzer
from AI.ANALYSIS.constraint_analyzer import ConstraintAnalyzer
from AI.ANALYSIS.design_analyzer import DesignAnalyzer
from AI.ANALYSIS.feature_detector import FeatureDetector
from AI.ANALYSIS.geometry_analyzer import GeometryAnalyzer
from AI.ANALYSIS.manufacturability_analyzer import ManufacturabilityAnalyzer
from AI.ANALYSIS.material_analyzer import MaterialAnalyzer
from AI.ANALYSIS.tolerance_analyzer import ToleranceAnalyzer
from AI.ANALYSIS.topology_analyzer import TopologyAnalyzer


@dataclass(slots=True)
class AnalysisRegistry:
    """Bundle enabled AI analyzers."""

    analyzers: dict[str, object] = field(
        default_factory=lambda: {
            "design": DesignAnalyzer(),
            "geometry": TopologyAnalyzer(),
            "geometry_named": GeometryAnalyzer(),
            "assembly": AssemblyAnalyzer(),
            "features": FeatureDetector(),
            "materials": MaterialAnalyzer(),
            "manufacturability": ManufacturabilityAnalyzer(),
            "constraints": ConstraintAnalyzer(),
            "tolerances": ToleranceAnalyzer(),
            "anomaly": AnomalyDetector(),
        }
    )
