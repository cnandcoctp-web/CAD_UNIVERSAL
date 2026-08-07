# Performance Hotspots

## Measured Baseline

- Full regression suite: `113 passed in 1.18s`
- Package build: passed
- Full import validation: passed

No failing performance checks were found during the audit, but several structural hotspots are evident.

## Hotspot 1: Full feature replay regeneration

- [MODELING/feature.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/MODELING/feature.py)

Why it matters:

- `FeatureManager.regenerate()` replays all active features linearly.
- There is no invalidation graph or partial regeneration scope.

Production risk:

- Large feature trees will pay global replay cost for local edits.

## Hotspot 2: Full-frame scene serialization

- [RENDERING/renderer.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/RENDERING/renderer.py)

Why it matters:

- Every render pass rebuilds serializable dictionaries for all visible objects.
- Visibility and bounds logic is primitive-specific and CPU-bound.

Production risk:

- Scene scale and viewport refresh cost will grow linearly with object count.

## Hotspot 3: Whole-project JSON persistence

- [IO/project_loader.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/IO/project_loader.py)
- [IO/project_saver.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/IO/project_saver.py)

Why it matters:

- Project load/save reads and writes complete JSON payloads.
- No chunking, compression, or partial loading is available.

Production risk:

- Large assemblies and simulation result sets will become IO-bound quickly.

## Hotspot 4: Framework-only simulation loop

- [SIMULATION/simulation_pipeline.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/SIMULATION/simulation_pipeline.py)

Why it matters:

- The current execution model is a step loop with checkpointing and sleep-based timing.
- It proves orchestration, not production solver throughput.

Production risk:

- Real solver workloads will need typed problem/result contracts and backend-specific execution management.

## Hotspot 5: Concrete cross-package data adaptation

- [AI/context_builder.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/AI/context_builder.py)
- [AI/ANALYSIS/design_snapshot_builder.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/AI/ANALYSIS/design_snapshot_builder.py)

Why it matters:

- AI constructs context directly from concrete Modeling and IO objects.
- This couples performance to peer data layouts and forces extra marshaling as the system grows.

## Conclusion

Current runtime performance is healthy for the deterministic baseline, but the architecture contains predictable scale bottlenecks in regeneration, rendering, persistence, and solver integration.