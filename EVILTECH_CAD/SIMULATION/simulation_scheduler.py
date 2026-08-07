"""Scheduler for queued simulation jobs."""

from __future__ import annotations

from concurrent.futures import Future
from threading import Lock

from SIMULATION.background_workers import BackgroundWorkers
from SIMULATION.simulation_pipeline import SimulationPipeline
from SIMULATION.simulation_queue import SimulationQueue


class SimulationScheduler:
    """Submit queued jobs to the background worker pool."""

    def __init__(self, queue: SimulationQueue, workers: BackgroundWorkers, pipeline: SimulationPipeline) -> None:
        self.queue = queue
        self.workers = workers
        self.pipeline = pipeline
        self._active: dict[str, Future[None]] = {}
        self._lock = Lock()

    def schedule(self, job_id: str) -> None:
        """Queue a job and dispatch work when a worker is available."""
        self.queue.enqueue(job_id)
        self.dispatch()

    def dispatch(self) -> None:
        """Dispatch as many queued jobs as the worker pool can accept."""
        with self._lock:
            capacity = self.workers.threading_manager.max_workers - len(self._active)
            while capacity > 0:
                next_job = self.queue.dequeue()
                if next_job is None:
                    break
                future = self.workers.submit(self.pipeline.run_job, next_job)
                self._active[next_job] = future
                future.add_done_callback(lambda _, job_id=next_job: self._complete(job_id))
                capacity -= 1

    def active_count(self) -> int:
        """Return the number of active worker futures."""
        with self._lock:
            return len(self._active)

    def _complete(self, job_id: str) -> None:
        with self._lock:
            self._active.pop(job_id, None)
        self.dispatch()