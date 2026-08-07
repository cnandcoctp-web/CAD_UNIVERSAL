"""Validation helpers for the AI pipeline."""

from __future__ import annotations

from AI.SCHEMAS.analysis_schema import DesignSnapshot
from UTILS.validators import ValidationReport


def validate_snapshot(snapshot: DesignSnapshot) -> ValidationReport:
    """Validate a design snapshot before analysis."""
    report = ValidationReport()
    if not snapshot.project_name:
        report.add_error("project_name must be non-empty")
    if not snapshot.geometry.entities:
        report.add_error("geometry dataset must contain at least one entity")
    return report
