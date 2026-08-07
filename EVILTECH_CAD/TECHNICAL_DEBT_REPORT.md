# Technical Debt Report

## High-Priority Debt

### Lightweight geometry and body model

- [GEOMETRY/topology.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/GEOMETRY/topology.py)
- [GEOMETRY/solid.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/GEOMETRY/solid.py)
- [MODELING/body.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/MODELING/body.py)

Debt: the current model stores vertices, simple mesh faces, or scalar body summaries instead of industrial topology.

Impact: persistent naming, kernel replacement, industrial import/export, and high-end simulation coupling are blocked.

### Full regeneration replay in Modeling

- [MODELING/feature.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/MODELING/feature.py)

Debt: regeneration replays features linearly and rebuilds summary state instead of using kernel transactions, invalidation scopes, and topology journals.

Impact: large models and feature edits will scale poorly.

### Framework-only simulation output

- [SIMULATION/simulation_pipeline.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/SIMULATION/simulation_pipeline.py)
- [SIMULATION/simulation_jobs.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/SIMULATION/simulation_jobs.py)

Debt: simulation is orchestration-only and explicitly retains future solver hooks.

Impact: no real FEA/CFD/thermal/EM solver integration exists yet.

### Placeholder persistence semantics

- [IO/project_loader.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/IO/project_loader.py)
- [IO/project_saver.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/IO/project_saver.py)
- [IO/project_models.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/IO/project_models.py)

Debt: `placeholder.json`, `cloud_sync`, and `team_collaboration` marker values are still present.

Impact: persistence format is stable for deterministic testing, but not complete for industrial collaboration or runtime integrations.

## Medium-Priority Debt

### Concrete package imports instead of adapters

See [ARCHITECTURE_VIOLATION_REPORT.md](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/ARCHITECTURE_VIOLATION_REPORT.md).

Impact: limits subsystem swapability and slows large-scale evolution.

### Headless UI framework only

- [UI/README.md](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/UI/README.md)

Debt: production desktop toolkit bindings do not exist.

Impact: acceptable for current deterministic baseline, but blocks true on-screen productization.

### Typed alias classes with empty bodies

- [SIMULATION/simulation_cache.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/SIMULATION/simulation_cache.py)
- [AI/STORAGE/state_cache.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/AI/STORAGE/state_cache.py)

Assessment: these are not dead code. They are typed aliases over shared cache infrastructure and remain acceptable.

## Dead Code and Duplicates Removed

Removed during audit because they were proven generated and unused by the live source tree:

- `build/`
- `dist/`
- `eviltech_cad.egg-info/`

After cleanup, exact duplicate live Python implementation clusters: `0`.

## Obsolete Compatibility Code

No obsolete runtime compatibility shim requiring removal was found in the live source.

## Conclusion

The dominant debt is architectural, not correctness-related. The repository is healthy enough for production development, but Version 2 should address kernel boundaries, adapter extraction, persistence depth, and solver architecture before pursuing industrial CAD scope.