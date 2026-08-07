"""Analysis schema definitions for the AI pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from AI.SCHEMAS.geometry_schema import GeometryDataset


@dataclass(slots=True)
class DesignSnapshot:
    """Full design snapshot consumed by analyzers and models."""

    project_name: str
    geometry: GeometryDataset
    feature_names: list[str] = field(default_factory=list)
    materials: list[str] = field(default_factory=list)
    constraint_summary: dict[str, Any] = field(default_factory=dict)
    assembly_summary: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AnalysisFinding:
    """A normalized finding emitted by an analyzer."""

    category: str
    severity: str
    message: str
    confidence: float
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AnalysisReport:
    """Aggregated analysis output for a design snapshot."""

    snapshot: DesignSnapshot
    findings: list[AnalysisFinding] = field(default_factory=list)
    confidence: float = 0.0
    metrics: dict[str, Any] = field(default_factory=dict)

    def finding_count(self) -> int:
        """Return the number of findings."""
        return len(self.findings)
