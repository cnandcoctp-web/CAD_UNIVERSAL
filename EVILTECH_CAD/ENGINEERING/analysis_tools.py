"""Engineering analysis helpers across disciplines."""

from __future__ import annotations

from ENGINEERING.engineering_models import DisciplineType


class EngineeringAnalysisTools:
    """Evaluate discipline-level metrics using deterministic heuristics."""

    def evaluate(self, discipline: DisciplineType, metrics: dict[str, float]) -> dict[str, object]:
        """Evaluate simple engineering metrics."""
        safety_factor = float(metrics.get("safety_factor", 1.5))
        compliance = float(metrics.get("compliance", 1.0))
        mass = float(metrics.get("mass_kg", 0.0))
        status = "pass" if safety_factor >= 1.5 and compliance >= 0.9 else "warning"
        return {
            "discipline": discipline.value,
            "status": status,
            "score": min(1.0, max(0.0, (safety_factor / 2.0 + compliance) / 2.0)),
            "mass_kg": mass,
        }