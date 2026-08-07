"""Validation engine for engineering calculation requests."""

from __future__ import annotations

import math

from ENGINEERING.engineering_models import EngineeringCalculationRequest, ValidationResponse
from ENGINEERING.engineering_registry import EngineeringRegistry


class EngineeringValidationEngine:
    """Validate engineering calculation inputs and outputs."""

    def __init__(self, registry: EngineeringRegistry) -> None:
        self.registry = registry

    def validate_request(self, request: EngineeringCalculationRequest) -> ValidationResponse:
        """Validate a calculation request."""
        spec = self.registry.get(request.discipline)
        errors: list[str] = []
        required = spec.required_inputs[request.calculation_name]
        for key in required:
            if key not in request.inputs:
                errors.append(f"Missing required input '{key}'")
                continue
            value = request.inputs[key]
            if not isinstance(value, (int, float)):
                errors.append(f"Input '{key}' must be numeric")
            elif not math.isfinite(float(value)):
                errors.append(f"Input '{key}' must be finite")
            elif float(value) <= 0.0:
                errors.append(f"Input '{key}' must be positive")
        return ValidationResponse(is_valid=not errors, errors=errors)