"""Core models for the engineering discipline modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from time import perf_counter
from typing import Any, Callable


class DisciplineType(str, Enum):
    """Supported engineering disciplines."""

    MECHANICAL_ENGINEERING = "mechanical_engineering"
    CIVIL_ENGINEERING = "civil_engineering"
    STRUCTURAL_ENGINEERING = "structural_engineering"
    ARCHITECTURE = "architecture"
    ELECTRICAL_ENGINEERING = "electrical_engineering"
    PLUMBING = "plumbing"
    HVAC = "hvac"
    MANUFACTURING = "manufacturing"
    MATERIALS_ENGINEERING = "materials_engineering"
    ROBOTICS = "robotics"
    AUTOMOTIVE_ENGINEERING = "automotive_engineering"
    AEROSPACE_ENGINEERING = "aerospace_engineering"
    THERMODYNAMICS = "thermodynamics"
    COMBUSTION_ENGINEERING = "combustion_engineering"
    FLUID_MECHANICS = "fluid_mechanics"
    ASTRONOMY = "astronomy"
    ORBITAL_MECHANICS = "orbital_mechanics"
    SCIENTIFIC_CALCULATIONS = "scientific_calculations"


@dataclass(slots=True)
class EngineeringCalculationRequest:
    """A calculation request bound to a discipline."""

    discipline: DisciplineType
    calculation_name: str
    inputs: dict[str, float]


@dataclass(slots=True)
class EngineeringCalculationResult:
    """Result of an engineering calculation."""

    discipline: DisciplineType
    calculation_name: str
    value: float
    unit: str
    valid: bool
    details: dict[str, Any] = field(default_factory=dict)
    duration_seconds: float = 0.0


@dataclass(slots=True)
class ValidationResponse:
    """Validation result for a request."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)


@dataclass(slots=True)
class DisciplineSpecification:
    """Complete specification for an engineering discipline."""

    discipline: DisciplineType
    default_calculation_name: str
    calculation_units: dict[str, str]
    formulas: dict[str, Callable[[dict[str, float]], float]]
    required_inputs: dict[str, tuple[str, ...]]
    sample_inputs: dict[str, dict[str, float]]
    design_rules: list[str]
    standards: list[str]
    library: dict[str, Any]
    future_interfaces: list[str]


class TimedCalculation:
    """Helper for timing deterministic engineering calculations."""

    @staticmethod
    def run(func: Callable[[dict[str, float]], float], inputs: dict[str, float]) -> tuple[float, float]:
        start = perf_counter()
        value = func(inputs)
        return value, perf_counter() - start