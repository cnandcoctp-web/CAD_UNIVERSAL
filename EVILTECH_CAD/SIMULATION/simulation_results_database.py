"""Persistent results database for simulation jobs."""

from __future__ import annotations

import json
from pathlib import Path
from threading import Lock

from SIMULATION.simulation_jobs import SimulationResult


class SimulationResultsDatabase:
    """Persist and retrieve simulation results."""

    def __init__(self, storage_root: Path) -> None:
        self.storage_root = Path(storage_root)
        self.storage_root.mkdir(parents=True, exist_ok=True)
        self._path = self.storage_root / "results.json"
        self._lock = Lock()
        self._results = self._load()

    def save(self, result: SimulationResult) -> None:
        """Store a simulation result and persist it to disk."""
        with self._lock:
            self._results[result.job_id] = result
            self._persist()

    def get(self, job_id: str) -> SimulationResult:
        """Return a stored simulation result."""
        with self._lock:
            return self._results[job_id]

    def all(self) -> list[SimulationResult]:
        """Return all stored simulation results."""
        with self._lock:
            return list(self._results.values())

    def _load(self) -> dict[str, SimulationResult]:
        if not self._path.exists():
            return {}
        payload = json.loads(self._path.read_text(encoding="utf-8"))
        return {job_id: SimulationResult.from_dict(data) for job_id, data in payload.items()}

    def _persist(self) -> None:
        self._path.write_text(
            json.dumps({job_id: result.to_dict() for job_id, result in self._results.items()}, indent=2, sort_keys=True),
            encoding="utf-8",
        )