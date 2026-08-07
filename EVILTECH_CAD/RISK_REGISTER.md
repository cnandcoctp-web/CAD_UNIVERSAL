# Risk Register

## High Risks

### 1. Geometry kernel depth risk

- Area: Geometry / Modeling
- Likelihood: High
- Impact: High
- Evidence: [GEOMETRY/topology.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/GEOMETRY/topology.py), [MODELING/body.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/MODELING/body.py)
- Risk: the current body representation is too lightweight for industrial CAD evolution.

### 2. Architecture boundary risk

- Area: Cross-package coupling
- Likelihood: High
- Impact: High
- Evidence: [ARCHITECTURE_VIOLATION_REPORT.md](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/ARCHITECTURE_VIOLATION_REPORT.md)
- Risk: direct peer implementation imports reduce swapability and increase refactor cost.

### 3. Persistence scalability risk

- Area: IO
- Likelihood: High
- Impact: High
- Evidence: [IO/project_loader.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/IO/project_loader.py), [IO/project_saver.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/IO/project_saver.py)
- Risk: whole-project JSON persistence will not scale to industrial assemblies.

### 4. Simulation capability risk

- Area: Simulation
- Likelihood: High
- Impact: Medium to High
- Evidence: [SIMULATION/simulation_pipeline.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/SIMULATION/simulation_pipeline.py)
- Risk: framework-only simulation may be mistaken for solver readiness.

## Medium Risks

### 5. Documentation drift risk

- Area: Documentation
- Likelihood: Medium
- Impact: Medium
- Evidence: multiple subsystem completion reports plus RC1 reports already exist
- Risk: without a baseline audit report, release and subsystem claims can drift over time.

### 6. Rendering scale risk

- Area: Rendering
- Likelihood: Medium
- Impact: Medium
- Evidence: [RENDERING/renderer.py](/workspaces/CAD_UNIVERSAL/EVILTECH_CAD/RENDERING/renderer.py)
- Risk: CPU-side frame serialization will bottleneck before GPU rendering exists.

### 7. Hidden artifact risk

- Area: Repository hygiene
- Likelihood: Medium
- Impact: Medium
- Evidence: generated `build/`, `dist/`, and `egg-info` artifacts were present during audit
- Risk: generated duplicates can pollute scans, inflate maintenance cost, and mask live source issues.

## Current Mitigations

- Full regression is green.
- Compile validation is green.
- Public imports and exports are green.
- Circular dependencies are eliminated.
- Generated duplicate artifacts were removed.

## Conclusion

No current risk blocks production development for Version 1. The highest risks are scale and architecture-evolution risks rather than immediate correctness risks.