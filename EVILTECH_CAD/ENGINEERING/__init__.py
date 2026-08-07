"""Engineering discipline modules for EvilTech CAD."""

from ENGINEERING.engineering_manager import EngineeringManager
from ENGINEERING.engineering_models import DisciplineType, EngineeringCalculationRequest, EngineeringCalculationResult

__all__ = ["DisciplineType", "EngineeringCalculationRequest", "EngineeringCalculationResult", "EngineeringManager"]