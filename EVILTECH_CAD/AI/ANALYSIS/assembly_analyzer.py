"""Assembly analyzer for the AI Engineering Assistant."""

from __future__ import annotations

from AI.SCHEMAS.analysis_schema import AnalysisFinding, DesignSnapshot


class AssemblyAnalyzer:
    """Analyze assembly composition and mate density."""

    def analyze(self, snapshot: DesignSnapshot) -> list[AnalysisFinding]:
        """Return assembly-related findings when assembly context exists."""
        component_count = int(snapshot.assembly_summary.get("components", 0))
        mate_count = int(snapshot.assembly_summary.get("mates", 0))
        findings: list[AnalysisFinding] = []
        if component_count >= 8 and mate_count <= 1:
            findings.append(AnalysisFinding("assembly", "warning", "Assembly complexity is increasing faster than mate definition coverage.", 0.69, {"components": component_count, "mates": mate_count}))
        return findings