"""Simulation integration helpers for engineering disciplines."""

from __future__ import annotations

from dataclasses import dataclass, field

from SIMULATION.simulation_jobs import SimulationJobConfig, SimulationType

from ENGINEERING.engineering_models import DisciplineType


@dataclass(slots=True)
class EngineeringSimulationRequest:
    """A discipline-scoped request for the simulation framework."""

    discipline: DisciplineType
    simulation_type: SimulationType
    parameters: dict[str, object] = field(default_factory=dict)

    def to_job_config(self, name: str, total_steps: int) -> SimulationJobConfig:
        """Convert the request to a simulation framework job config."""
        payload = dict(self.parameters)
        payload["discipline"] = self.discipline.value
        return SimulationJobConfig(name=name, simulation_type=self.simulation_type, total_steps=total_steps, parameters=payload)


class EngineeringSimulationIntegration:
    """Build simulation requests from engineering modules."""

    def build_request(self, discipline: DisciplineType, simulation_type: SimulationType, parameters: dict[str, object]) -> EngineeringSimulationRequest:
        """Create a simulation integration request."""
        return EngineeringSimulationRequest(discipline=discipline, simulation_type=simulation_type, parameters=dict(parameters))