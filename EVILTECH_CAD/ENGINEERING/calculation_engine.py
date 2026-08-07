"""Deterministic engineering calculation engine."""

from __future__ import annotations

from ENGINEERING.engineering_models import EngineeringCalculationRequest, EngineeringCalculationResult, TimedCalculation
from ENGINEERING.engineering_registry import EngineeringRegistry


class EngineeringCalculationEngine:
    """Run deterministic engineering calculations by discipline."""

    def __init__(self, registry: EngineeringRegistry) -> None:
        self.registry = registry

    def evaluate(self, request: EngineeringCalculationRequest) -> EngineeringCalculationResult:
        """Evaluate a calculation request."""
        spec = self.registry.get(request.discipline)
        formula = spec.formulas[request.calculation_name]
        value, duration = TimedCalculation.run(formula, request.inputs)
        return EngineeringCalculationResult(
            discipline=request.discipline,
            calculation_name=request.calculation_name,
            value=float(value),
            unit=spec.calculation_units[request.calculation_name],
            valid=True,
            details={"inputs": dict(request.inputs)},
            duration_seconds=duration,
        )