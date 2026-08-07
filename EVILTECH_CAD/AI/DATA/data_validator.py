"""Validation helpers for AI data loading."""

from __future__ import annotations

from AI.SCHEMAS.geometry_schema import GeometryDataset
from UTILS.validators import ValidationReport


class DataValidator:
    """Validate AI-ready datasets."""

    def validate_geometry(self, dataset: GeometryDataset) -> ValidationReport:
        """Validate a geometry dataset."""
        report = ValidationReport()
        if not dataset.entities:
            report.add_error("Geometry dataset must contain at least one entity")
        if dataset.total_volume() < 0.0:
            report.add_error("Geometry dataset volume must be non-negative")
        return report
