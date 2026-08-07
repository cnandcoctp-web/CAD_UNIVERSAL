"""Top-level orchestration for engineering discipline modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ENGINEERING.ai_integration import EngineeringAIIntegration
from ENGINEERING.analysis_tools import EngineeringAnalysisTools
from ENGINEERING.calculation_engine import EngineeringCalculationEngine
from ENGINEERING.design_rules import EngineeringDesignRules
from ENGINEERING.discipline_libraries import DisciplineLibraries
from ENGINEERING.engineering_models import DisciplineType, EngineeringCalculationRequest, EngineeringCalculationResult
from ENGINEERING.engineering_registry import EngineeringRegistry
from ENGINEERING.future_expansion_interfaces import FutureExpansionInterfaces
from ENGINEERING.material_integration import EngineeringMaterialIntegration
from ENGINEERING.optimization_utilities import EngineeringOptimizationUtilities
from ENGINEERING.report_generator import EngineeringReportGenerator
from ENGINEERING.sample_project_generator import SampleEngineeringProjectGenerator
from ENGINEERING.simulation_integration import EngineeringSimulationIntegration
from ENGINEERING.standards_framework import IndustryStandardsFramework
from ENGINEERING.validation_engine import EngineeringValidationEngine


@dataclass(slots=True)
class EngineeringManager:
    """Own the engineering discipline infrastructure."""

    storage_root: Path
    registry: EngineeringRegistry = field(default_factory=EngineeringRegistry)
    calculation_engine: EngineeringCalculationEngine = field(init=False)
    validation_engine: EngineeringValidationEngine = field(init=False)
    design_rules: EngineeringDesignRules = field(init=False)
    standards_framework: IndustryStandardsFramework = field(init=False)
    material_integration: EngineeringMaterialIntegration = field(init=False)
    analysis_tools: EngineeringAnalysisTools = field(init=False)
    optimization_utilities: EngineeringOptimizationUtilities = field(init=False)
    discipline_libraries: DisciplineLibraries = field(init=False)
    future_expansion_interfaces: FutureExpansionInterfaces = field(init=False)
    sample_project_generator: SampleEngineeringProjectGenerator = field(init=False)
    report_generator: EngineeringReportGenerator = field(init=False)
    ai_integration: EngineeringAIIntegration = field(init=False)
    simulation_integration: EngineeringSimulationIntegration = field(init=False)

    def __post_init__(self) -> None:
        self.storage_root = Path(self.storage_root)
        self.storage_root.mkdir(parents=True, exist_ok=True)
        self.calculation_engine = EngineeringCalculationEngine(self.registry)
        self.validation_engine = EngineeringValidationEngine(self.registry)
        self.design_rules = EngineeringDesignRules(self.registry)
        self.standards_framework = IndustryStandardsFramework(self.registry)
        self.material_integration = EngineeringMaterialIntegration()
        self.analysis_tools = EngineeringAnalysisTools()
        self.optimization_utilities = EngineeringOptimizationUtilities()
        self.discipline_libraries = DisciplineLibraries(self.registry)
        self.future_expansion_interfaces = FutureExpansionInterfaces(self.registry)
        self.sample_project_generator = SampleEngineeringProjectGenerator(self.registry)
        self.report_generator = EngineeringReportGenerator()
        self.ai_integration = EngineeringAIIntegration()
        self.simulation_integration = EngineeringSimulationIntegration()

    def create_calculation_request(self, discipline: DisciplineType, calculation_name: str, inputs: dict[str, float]) -> EngineeringCalculationRequest:
        """Create an engineering calculation request."""
        return EngineeringCalculationRequest(discipline=discipline, calculation_name=calculation_name, inputs=dict(inputs))

    def run_calculation(self, request: EngineeringCalculationRequest) -> EngineeringCalculationResult:
        """Validate and run a calculation request."""
        validation = self.validation_engine.validate_request(request)
        if not validation.is_valid:
            raise ValueError("Invalid engineering calculation request: " + "; ".join(validation.errors))
        return self.calculation_engine.evaluate(request)

    def validation_summary(self, results: list[EngineeringCalculationResult]) -> dict[str, float | int]:
        """Return a validation summary for a set of results."""
        valid_count = sum(1 for result in results if result.valid)
        return {
            "valid_results": valid_count,
            "invalid_results": len(results) - valid_count,
            "average_duration_seconds": sum(result.duration_seconds for result in results) / len(results) if results else 0.0,
        }