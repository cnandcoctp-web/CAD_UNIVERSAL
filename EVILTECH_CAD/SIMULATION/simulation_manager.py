"""Simulation manager and orchestration for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from threading import Condition, Event, Lock
import weakref

from SIMULATION.background_workers import BackgroundWorkers
from SIMULATION.job_recovery_manager import JobRecoveryManager
from SIMULATION.multithreading_manager import MultiThreadingManager
from SIMULATION.progress_monitor import ProgressMonitor
from SIMULATION.resource_monitor import ResourceMonitor
from SIMULATION.simulation_cache import SimulationCache
from SIMULATION.simulation_history import SimulationHistory
from SIMULATION.simulation_jobs import SimulationJob, SimulationJobConfig, SimulationState
from SIMULATION.simulation_logger import SimulationLogger
from SIMULATION.simulation_pipeline import SimulationPipeline
from SIMULATION.simulation_queue import SimulationQueue
from SIMULATION.simulation_results_database import SimulationResultsDatabase
from SIMULATION.simulation_scheduler import SimulationScheduler
from SIMULATION.simulation_state_manager import SimulationStateManager


@dataclass(slots=True)
class JobControl:
    """In-memory runtime control flags for a simulation job."""

    paused: bool = False
    cancelled: bool = False
    done_event: Event = field(default_factory=Event)
    condition: Condition = field(default_factory=Condition)


class SimulationManager:
    """Own simulation jobs, scheduling, execution, persistence, and monitoring."""

    def __init__(self, storage_root: Path, max_workers: int = 2) -> None:
        self.storage_root = Path(storage_root)
        self.storage_root.mkdir(parents=True, exist_ok=True)
        self._jobs: dict[str, SimulationJob] = {}
        self._controls: dict[str, JobControl] = {}
        self._lock = Lock()
        self.queue = SimulationQueue()
        self.cache = SimulationCache()
        self.history = SimulationHistory()
        self.state_manager = SimulationStateManager()
        self.logger = SimulationLogger()
        self.results_database = SimulationResultsDatabase(self.storage_root / "results")
        self.threading_manager = MultiThreadingManager(max_workers=max_workers)
        self.workers = BackgroundWorkers(self.threading_manager)
        self.pipeline = SimulationPipeline(self)
        self.scheduler = SimulationScheduler(self.queue, self.workers, self.pipeline)
        self.progress_monitor = ProgressMonitor(self.state_manager)
        self.resource_monitor = ResourceMonitor(self.state_manager)
        self.recovery_manager = JobRecoveryManager(self, self.storage_root / "checkpoints")
        self._finalizer = weakref.finalize(self, type(self)._shutdown_pool, self.threading_manager)

    def create_job(self, config: SimulationJobConfig) -> SimulationJob:
        """Create and register a simulation job."""
        job = SimulationJob.create(config)
        self.register_restored_job(job, SimulationState(job_id=job.job_id, status="created", current_step=0, total_steps=config.total_steps, progress=0.0, message="Created"))
        self.history.record(job.job_id, "created")
        self.logger.log(job.job_id, "created", "Simulation job created", simulation_type=config.simulation_type.value)
        return job

    def register_restored_job(self, job: SimulationJob, state: SimulationState) -> None:
        """Register a new or restored job and its state."""
        with self._lock:
            self._jobs[job.job_id] = job
            self._controls[job.job_id] = JobControl()
        self.state_manager.register(state)
        self.logger.log(job.job_id, "registered", "Simulation job registered", status=state.status)

    def get_job(self, job_id: str) -> SimulationJob:
        """Return a job by identifier."""
        return self._jobs[job_id]

    def get_control(self, job_id: str) -> JobControl:
        """Return runtime control data for a job."""
        return self._controls[job_id]

    def start_job(self, job_id: str) -> None:
        """Queue a created or restored job for execution."""
        state = self.state_manager.get(job_id)
        if state.status in {"running", "completed", "cancelled", "failed"}:
            return
        self.state_manager.update(job_id, status="queued", message="Queued for execution")
        self.history.record(job_id, "queued")
        self.logger.log(job_id, "queued", "Simulation queued")
        self.scheduler.schedule(job_id)

    def pause_job(self, job_id: str) -> None:
        """Pause a running job."""
        control = self.get_control(job_id)
        control.paused = True
        self.state_manager.update(job_id, status="paused", message="Paused by user")
        self.history.record(job_id, "paused")
        self.logger.log(job_id, "paused", "Simulation paused")

    def resume_job(self, job_id: str) -> None:
        """Resume a paused job."""
        control = self.get_control(job_id)
        with control.condition:
            control.paused = False
            control.condition.notify_all()
        state = self.state_manager.get(job_id)
        if state.status == "paused":
            self.state_manager.update(job_id, status="queued", message="Resumed")
        self.history.record(job_id, "resumed")
        self.logger.log(job_id, "resumed", "Simulation resumed")
        if self.scheduler.active_count() == 0 or state.status == "paused":
            self.scheduler.schedule(job_id)
        self.scheduler.dispatch()

    def cancel_job(self, job_id: str) -> None:
        """Cancel a queued, running, or paused job."""
        state = self.state_manager.get(job_id)
        control = self.get_control(job_id)
        if self.queue.remove(job_id):
            control.cancelled = True
            control.done_event.set()
            self.state_manager.update(job_id, status="cancelled", message="Cancelled while queued")
            self.history.record(job_id, "cancelled")
            self.logger.log(job_id, "cancelled", "Simulation cancelled while queued")
            return
        if state.status in {"completed", "cancelled", "failed"}:
            return
        with control.condition:
            control.cancelled = True
            control.paused = False
            control.condition.notify_all()
        self.history.record(job_id, "cancelled")
        self.logger.log(job_id, "cancelled", "Simulation cancellation requested")

    def wait_for_job(self, job_id: str, timeout_seconds: float = 10.0) -> None:
        """Wait for a job to reach a terminal state."""
        if not self.get_control(job_id).done_event.wait(timeout_seconds):
            raise TimeoutError(f"Timed out waiting for job '{job_id}'")

    def wait_for_progress(self, job_id: str, minimum_progress: float, timeout_seconds: float = 5.0) -> None:
        """Wait until a job reaches the requested progress threshold."""
        self.progress_monitor.wait_for_progress(job_id, minimum_progress, timeout_seconds)

    def scalability_report(self) -> dict[str, float | int]:
        """Return aggregate performance and completion metrics."""
        results = self.results_database.all()
        completed = [result for result in results if result.status == "completed"]
        failed = [result for result in results if result.status == "failed"]
        return {
            "completed_jobs": len(completed),
            "failed_jobs": len(failed),
            "average_duration_seconds": sum(result.duration_seconds for result in results) / len(results) if results else 0.0,
        }

    def shutdown(self) -> None:
        """Shut down background worker infrastructure."""
        self._shutdown_pool(self.threading_manager)
        if self._finalizer.alive:
            self._finalizer.detach()

    @staticmethod
    def _shutdown_pool(threading_manager: MultiThreadingManager) -> None:
        """Shut down the background thread pool safely."""
        threading_manager.shutdown()