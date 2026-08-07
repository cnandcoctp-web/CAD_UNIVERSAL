"""Simulation job, state, and result models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class SimulationType(str, Enum):
    """Supported simulation framework types."""

    STRUCTURAL_ANALYSIS = "structural_analysis"
    STATIC_STRESS = "static_stress"
    DYNAMIC_STRESS = "dynamic_stress"
    THERMAL_ANALYSIS = "thermal_analysis"
    HEAT_TRANSFER = "heat_transfer"
    FLUID_DYNAMICS_FRAMEWORK = "fluid_dynamics_framework"
    COMBUSTION_FRAMEWORK = "combustion_framework"
    MOTION_SIMULATION = "motion_simulation"
    KINEMATICS = "kinematics"
    DYNAMICS = "dynamics"
    COLLISION_DETECTION = "collision_detection"
    MATERIAL_BEHAVIOUR = "material_behaviour"
    FATIGUE_ANALYSIS = "fatigue_analysis"
    ORBITAL_MECHANICS_FRAMEWORK = "orbital_mechanics_framework"
    ELECTROMAGNETIC_FRAMEWORK = "electromagnetic_framework"


@dataclass(slots=True)
class SimulationJobConfig:
    """Static configuration for a simulation job."""

    name: str
    simulation_type: SimulationType
    total_steps: int
    parameters: dict[str, Any] = field(default_factory=dict)
    checkpoint_interval: int = 5
    future_cloud_offload_hook: str | None = None

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("name must be non-empty")
        if not isinstance(self.simulation_type, SimulationType):
            self.simulation_type = SimulationType(self.simulation_type)
        if self.total_steps <= 0:
            raise ValueError("total_steps must be positive")
        if self.checkpoint_interval <= 0:
            raise ValueError("checkpoint_interval must be positive")

    def to_dict(self) -> dict[str, Any]:
        """Serialize the config to a dictionary."""
        return {
            "name": self.name,
            "simulation_type": self.simulation_type.value,
            "total_steps": self.total_steps,
            "parameters": dict(self.parameters),
            "checkpoint_interval": self.checkpoint_interval,
            "future_cloud_offload_hook": self.future_cloud_offload_hook,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SimulationJobConfig":
        """Deserialize config from a dictionary."""
        return cls(
            name=str(payload["name"]),
            simulation_type=SimulationType(payload["simulation_type"]),
            total_steps=int(payload["total_steps"]),
            parameters=dict(payload.get("parameters", {})),
            checkpoint_interval=int(payload.get("checkpoint_interval", 5)),
            future_cloud_offload_hook=payload.get("future_cloud_offload_hook"),
        )


@dataclass(slots=True)
class SimulationJob:
    """A queued or running simulation job."""

    job_id: str
    config: SimulationJobConfig
    cache_key: str
    created_at: str = field(default_factory=_utc_now)

    @classmethod
    def create(cls, config: SimulationJobConfig) -> "SimulationJob":
        """Create a new simulation job from config."""
        job_id = str(uuid4())
        cache_key = f"simulation:{config.simulation_type.value}:{config.name}:{config.total_steps}"
        return cls(job_id=job_id, config=config, cache_key=cache_key)


@dataclass(slots=True)
class SimulationState:
    """Mutable state of a simulation job."""

    job_id: str
    status: str
    current_step: int
    total_steps: int
    progress: float = 0.0
    message: str = ""
    updated_at: str = field(default_factory=_utc_now)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the state."""
        return {
            "job_id": self.job_id,
            "status": self.status,
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "progress": self.progress,
            "message": self.message,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SimulationState":
        """Deserialize state."""
        return cls(
            job_id=str(payload["job_id"]),
            status=str(payload["status"]),
            current_step=int(payload["current_step"]),
            total_steps=int(payload["total_steps"]),
            progress=float(payload.get("progress", 0.0)),
            message=str(payload.get("message", "")),
            updated_at=str(payload.get("updated_at", _utc_now())),
        )


@dataclass(slots=True)
class SimulationResult:
    """Persisted result of a simulation job."""

    job_id: str
    status: str
    started_at: str
    finished_at: str
    duration_seconds: float
    output: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the result."""
        return {
            "job_id": self.job_id,
            "status": self.status,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_seconds": self.duration_seconds,
            "output": dict(self.output),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SimulationResult":
        """Deserialize a result."""
        return cls(
            job_id=str(payload["job_id"]),
            status=str(payload["status"]),
            started_at=str(payload["started_at"]),
            finished_at=str(payload["finished_at"]),
            duration_seconds=float(payload.get("duration_seconds", 0.0)),
            output=dict(payload.get("output", {})),
        )