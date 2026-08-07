"""Engineering knowledge base for the AI Engineering Assistant."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class EngineeringDomain:
    """A supported engineering discipline."""

    name: str
    summary: str
    capabilities: tuple[str, ...] = field(default_factory=tuple)


class EngineeringKnowledgeBase:
    """Domain and capability knowledge for assistant prompting and reporting."""

    def __init__(self) -> None:
        capability_set = (
            "design_review",
            "design_suggestions",
            "error_detection",
            "constraint_explanations",
            "manufacturing_advice",
            "material_recommendations",
            "optimization_suggestions",
            "tolerance_analysis",
            "engineering_calculations",
            "project_guidance",
            "design_documentation",
        )
        self._domains: dict[str, EngineeringDomain] = {
            "mechanical_engineering": EngineeringDomain("mechanical_engineering", "Parts, assemblies, motion, and manufacturable geometry.", capability_set),
            "structural_engineering": EngineeringDomain("structural_engineering", "Load paths, rigidity, and structural efficiency.", capability_set),
            "architecture": EngineeringDomain("architecture", "Spatial design, constructability, and documentation clarity.", capability_set),
            "civil_engineering": EngineeringDomain("civil_engineering", "Infrastructure-oriented geometry and buildability review.", capability_set),
            "electrical_engineering": EngineeringDomain("electrical_engineering", "Component packaging, routing space, and serviceability.", capability_set),
            "plumbing": EngineeringDomain("plumbing", "Flow paths, clearances, and installation constraints.", capability_set),
            "manufacturing": EngineeringDomain("manufacturing", "Process suitability, production efficiency, and tolerance cost.", capability_set),
            "thermodynamics": EngineeringDomain("thermodynamics", "Thermal pathways, surfaces, and heat-transfer implications.", capability_set),
            "combustion": EngineeringDomain("combustion", "High-temperature and combustion-adjacent design considerations.", capability_set),
            "fluid_mechanics": EngineeringDomain("fluid_mechanics", "Flow geometry, pressure loss risk, and channel design.", capability_set),
            "astronomy": EngineeringDomain("astronomy", "Observation hardware context and precision-driven structures.", capability_set),
            "orbital_mechanics": EngineeringDomain("orbital_mechanics", "Spacecraft packaging, mass sensitivity, and orbital hardware context.", capability_set),
            "material_science": EngineeringDomain("material_science", "Material behavior, process compatibility, and lifecycle tradeoffs.", capability_set),
            "physics": EngineeringDomain("physics", "Dimensional consistency and physically sensible design tradeoffs.", capability_set),
            "mathematics": EngineeringDomain("mathematics", "Formal reasoning, optimization structure, and quantitative explanation.", capability_set),
        }
        self._future_integrations = {
            "simulation_analysis": "planned",
            "cloud_ai": "planned",
            "vision_models": "planned",
            "voice_assistant": "planned",
            "multi_agent_collaboration": "planned",
        }

    def domain_names(self) -> list[str]:
        """Return supported engineering-domain names."""
        return sorted(self._domains)

    def get_domain(self, name: str) -> EngineeringDomain:
        """Return an engineering domain description."""
        return self._domains[name]

    def future_integrations(self) -> dict[str, str]:
        """Return future-ready integration markers."""
        return dict(self._future_integrations)