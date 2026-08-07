"""Geometry analyzer for the AI Engineering Assistant."""

from __future__ import annotations

from AI.ANALYSIS.topology_analyzer import TopologyAnalyzer
from AI.SCHEMAS.analysis_schema import AnalysisFinding, DesignSnapshot


class GeometryAnalyzer:
    """Analyze geometry complexity and surface-level shape risk."""

    def __init__(self) -> None:
        self.topology = TopologyAnalyzer()

    def analyze(self, snapshot: DesignSnapshot) -> list[AnalysisFinding]:
        """Return geometry-related findings."""
        return self.topology.analyze(snapshot)