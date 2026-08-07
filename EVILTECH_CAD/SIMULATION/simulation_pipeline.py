"""Background execution pipeline for simulation jobs."""

from __future__ import annotations

from datetime import datetime, timezone
from time import monotonic, sleep

from SIMULATION.simulation_jobs import SimulationResult


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class SimulationPipeline:
    """Execute generic framework simulations without discipline-specific math."""

    def __init__(self, manager: "SimulationManager") -> None:
        self.manager = manager

    def run_job(self, job_id: str) -> None:
        """Run a job from its current step to completion, cancellation, or failure."""
        job = self.manager.get_job(job_id)
        control = self.manager.get_control(job_id)
        state = self.manager.state_manager.peek(job_id)
        step_delay = float(job.config.parameters.get("step_delay", 0.001))
        checkpoint_interval = int(job.config.parameters.get("checkpoint_interval", job.config.checkpoint_interval))
        started_at = _utc_now()
        started_clock = monotonic()
        self.manager.state_manager.update(job_id, status="running", message="Simulation running")
        self.manager.history.record(job_id, "running", step=state.current_step)
        self.manager.logger.log(job_id, "running", "Simulation started", simulation_type=job.config.simulation_type.value)

        try:
            while state.current_step < state.total_steps:
                with control.condition:
                    while control.paused and not control.cancelled:
                        self.manager.state_manager.update(job_id, status="paused", message="Simulation paused")
                        control.condition.wait(timeout=0.05)
                    if control.cancelled:
                        return self._finalize(job_id, started_at, started_clock, status="cancelled")

                sleep(step_delay)
                state = self.manager.state_manager.peek(job_id)
                next_step = state.current_step + 1
                progress = next_step / state.total_steps
                self.manager.state_manager.update(job_id, current_step=next_step, progress=progress, status="running", updated_at=_utc_now())
                self.manager.history.record(job_id, "running", step=next_step, progress=progress)
                if checkpoint_interval and next_step % checkpoint_interval == 0:
                    self.manager.recovery_manager.save_checkpoint(job_id, automatic=True)

            self._finalize(job_id, started_at, started_clock, status="completed")
        except Exception as exc:
            self.manager.state_manager.update(job_id, status="failed", message=str(exc), updated_at=_utc_now())
            self.manager.history.record(job_id, "failed", error=str(exc))
            self.manager.logger.log(job_id, "failed", "Simulation failed", error=str(exc))
            control.done_event.set()
            raise

    def _finalize(self, job_id: str, started_at: str, started_clock: float, status: str) -> None:
        job = self.manager.get_job(job_id)
        state = self.manager.state_manager.peek(job_id)
        duration = monotonic() - started_clock
        finished_at = _utc_now()
        self.manager.state_manager.update(job_id, status=status, progress=state.current_step / state.total_steps, updated_at=finished_at)
        output = {
            "simulation_type": job.config.simulation_type.value,
            "steps_completed": state.current_step,
            "total_steps": state.total_steps,
            "parameters": dict(job.config.parameters),
            "cloud_offload_hook": job.config.future_cloud_offload_hook,
            "framework_only": True,
        }
        result = SimulationResult(
            job_id=job_id,
            status=status,
            started_at=started_at,
            finished_at=finished_at,
            duration_seconds=duration,
            output=output,
        )
        self.manager.results_database.save(result)
        self.manager.cache.set(job.cache_key, result)
        self.manager.history.record(job_id, status, duration_seconds=duration)
        self.manager.logger.log(job_id, status, f"Simulation {status}", duration_seconds=duration)
        self.manager.get_control(job_id).done_event.set()