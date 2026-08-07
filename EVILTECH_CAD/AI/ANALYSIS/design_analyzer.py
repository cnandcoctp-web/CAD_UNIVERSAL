"""Top-level design analyzer for the AI Engineering Assistant."""

from __future__ import annotations

from AI.ANALYSIS.anomaly_detector import AnomalyDetector
from AI.ANALYSIS.assembly_analyzer import AssemblyAnalyzer
from AI.ANALYSIS.constraint_analyzer import ConstraintAnalyzer
from AI.ANALYSIS.feature_detector import FeatureDetector
from AI.ANALYSIS.geometry_analyzer import GeometryAnalyzer
from AI.ANALYSIS.manufacturability_analyzer import ManufacturabilityAnalyzer
from AI.ANALYSIS.material_analyzer import MaterialAnalyzer
from AI.ANALYSIS.tolerance_analyzer import ToleranceAnalyzer
from AI.SCHEMAS.analysis_schema import AnalysisFinding, DesignSnapshot


class DesignAnalyzer:
    """Run the supported engineering analyzers over a design snapshot."""

    def __init__(self) -> None:
        self.geometry = GeometryAnalyzer()
        self.assembly = AssemblyAnalyzer()
        self.constraints = ConstraintAnalyzer()
        self.materials = MaterialAnalyzer()
        self.tolerances = ToleranceAnalyzer()
        self.manufacturability = ManufacturabilityAnalyzer()
        self.features = FeatureDetector()
        self.anomalies = AnomalyDetector()

    def analyze(self, snapshot: DesignSnapshot, enabled: list[str] | None = None) -> list[AnalysisFinding]:
        """Analyze a design snapshot with the enabled analyzer set."""
        enabled_set = set(enabled or ["geometry", "assembly", "constraints", "materials", "tolerances", "manufacturability", "features", "anomaly"])
        findings: list[AnalysisFinding] = []
        if "geometry" in enabled_set:
            findings.extend(self.geometry.analyze(snapshot))
        if "assembly" in enabled_set:
            findings.extend(self.assembly.analyze(snapshot))
        if "constraints" in enabled_set:
            findings.extend(self.constraints.analyze(snapshot))
        if "materials" in enabled_set:
            findings.extend(self.materials.analyze(snapshot))
        if "tolerances" in enabled_set:
            findings.extend(self.tolerances.analyze(snapshot))
        if "manufacturability" in enabled_set:
            findings.extend(self.manufacturability.analyze(snapshot))
        if "features" in enabled_set:
            findings.extend(self.features.analyze(snapshot))
        if "anomaly" in enabled_set:
            findings.extend(self.anomalies.analyze(snapshot))
        return findings