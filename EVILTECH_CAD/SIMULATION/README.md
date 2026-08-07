# Simulation Framework

The `SIMULATION` package provides a headless engineering simulation framework
for job orchestration, scheduling, background execution, checkpointing,
recovery, persistence, monitoring, and multi-job concurrency.

This package intentionally does not implement domain-specific engineering
equations. It supplies the infrastructure needed to run future structural,
thermal, fluid, motion, orbital, and electromagnetic solvers safely and
asynchronously.