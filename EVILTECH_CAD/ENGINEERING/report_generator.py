"""Engineering report generation."""

from __future__ import annotations

from ENGINEERING.engineering_models import EngineeringCalculationResult


class EngineeringReportGenerator:
    """Generate deterministic engineering reports."""

    def generate(self, project_id: str, project_payload: dict[str, object], result: EngineeringCalculationResult) -> dict[str, object]:
        """Generate a report for a project and calculation result."""
        return {
            "project_id": project_id,
            "discipline": project_payload["discipline"],
            "project_name": project_payload["project_name"],
            "calculation": {
                "name": result.calculation_name,
                "value": result.value,
                "unit": result.unit,
                "valid": result.valid,
            },
            "standards": list(project_payload["standards"]),
            "design_rules": list(project_payload["design_rules"]),
        }