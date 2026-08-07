"""Checkpoint and recovery support for simulation jobs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from SIMULATION.simulation_jobs import SimulationJob, SimulationJobConfig, SimulationState


class JobRecoveryManager:
    """Persist and restore simulation job checkpoints."""

    def __init__(self, manager: "SimulationManager", storage_root: Path) -> None:
        self.manager = manager
        self.storage_root = Path(storage_root)
        self.storage_root.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(self, job_id: str, automatic: bool = False) -> Path:
        """Write a checkpoint for a job's current config and state."""
        job = self.manager.get_job(job_id)
        state = self.manager.state_manager.get(job_id)
        target = self.storage_root / f"{job_id}.json"
        payload = {
            "job": {
                "job_id": job.job_id,
                "cache_key": job.cache_key,
                "created_at": job.created_at,
                "config": job.config.to_dict(),
            },
            "state": state.to_dict(),
            "automatic": automatic,
        }
        target.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        return target

    def restore_job(self, checkpoint_path: Path) -> SimulationJob:
        """Restore a checkpointed job into the attached manager."""
        payload = json.loads(Path(checkpoint_path).read_text(encoding="utf-8"))
        job_payload = payload["job"]
        job = SimulationJob(
            job_id=str(job_payload["job_id"]),
            cache_key=str(job_payload["cache_key"]),
            created_at=str(job_payload["created_at"]),
            config=SimulationJobConfig.from_dict(job_payload["config"]),
        )
        state = SimulationState.from_dict(payload["state"])
        self.manager.register_restored_job(job, state)
        return job