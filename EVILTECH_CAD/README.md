# EvilTech CAD

EvilTech CAD is a deterministic, headless engineering operating system that integrates the completed foundation, geometry, modeling, constraints, IO, rendering, AI, simulation, and engineering-discipline subsystems into one release-candidate workflow.

Current release candidate: `1.0.0rc1`

## Release Candidate Scope

RC1 focuses on system integration and release readiness.

- Production-oriented startup and shutdown lifecycle
- Deterministic project persistence and recovery
- Constraint, modeling, and rendering validation
- Advisory AI engineering review workflow
- Framework-only simulation orchestration
- Engineering-discipline calculations, reporting, and simulation adapters
- Headless regression, integration, stress, and release-candidate validation suites

## Requirements

- Python 3.12 or later
- `numpy`
- `scipy`

Install runtime dependencies with:

```bash
pip install -r requirements.txt
```

## Launch

Run the application entry point:

```bash
python main.py
```

Inspect the release version:

```bash
python main.py --version
```

## Build

Build an installable wheel from the repository root:

```bash
python -m pip wheel . --no-deps -w dist
```

This produces the RC1 packaging artifact without changing subsystem architecture.

## Validation

Run the complete regression suite:

```bash
pytest -q
```

Run the release-candidate integration suite:

```bash
pytest -q TEST/test_release_candidate.py
```

Run the engineering-module suite:

```bash
pytest -q TEST/test_engineering.py
```

## Documentation Index

System architecture and contracts:

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [INTERFACE_CONTRACTS.md](INTERFACE_CONTRACTS.md)
- [TECHNOLOGY_STACK.md](TECHNOLOGY_STACK.md)
- [ENGINEERING_REVIEW.md](ENGINEERING_REVIEW.md)

Subsystem completion reports:

- [FOUNDATION_VALIDATION_REPORT.md](FOUNDATION_VALIDATION_REPORT.md)
- [PROJECT_SYSTEM_COMPLETION_REPORT.md](PROJECT_SYSTEM_COMPLETION_REPORT.md)
- [CONSTRAINT_ENGINE_COMPLETION_REPORT.md](CONSTRAINT_ENGINE_COMPLETION_REPORT.md)
- [GEOMETRY_KERNEL_COMPLETION_REPORT.md](GEOMETRY_KERNEL_COMPLETION_REPORT.md)
- [MATH_ENGINE_COMPLETION_REPORT.md](MATH_ENGINE_COMPLETION_REPORT.md)
- [MODELING_ENGINE_COMPLETION_REPORT.md](MODELING_ENGINE_COMPLETION_REPORT.md)
- [RENDERING_COMPLETION_REPORT.md](RENDERING_COMPLETION_REPORT.md)
- [UI_COMPLETION_REPORT.md](UI_COMPLETION_REPORT.md)
- [AI_ENGINEERING_COMPLETION_REPORT.md](AI_ENGINEERING_COMPLETION_REPORT.md)
- [SIMULATION_FRAMEWORK_COMPLETION_REPORT.md](SIMULATION_FRAMEWORK_COMPLETION_REPORT.md)
- [ENGINEERING_MODULES_COMPLETION_REPORT.md](ENGINEERING_MODULES_COMPLETION_REPORT.md)

Release-candidate reports:

- `ARCHITECTURE_COMPLIANCE_REPORT.md`
- `PERFORMANCE_REPORT.md`
- `SECURITY_REPORT.md`
- `TEST_COVERAGE_REPORT.md`
- `KNOWN_ISSUES_REPORT.md`
- `RELEASE_NOTES_RC1.md`
- `ENGINEERING_READINESS_REPORT.md`
- `RELEASE_CANDIDATE_REPORT.md`

Production baseline audit reports:

- [REPOSITORY_HEALTH_REPORT.md](REPOSITORY_HEALTH_REPORT.md)
- [ARCHITECTURE_VIOLATION_REPORT.md](ARCHITECTURE_VIOLATION_REPORT.md)
- [TECHNICAL_DEBT_REPORT.md](TECHNICAL_DEBT_REPORT.md)
- [PERFORMANCE_HOTSPOTS.md](PERFORMANCE_HOTSPOTS.md)
- [RISK_REGISTER.md](RISK_REGISTER.md)
- [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md)
- [COVERAGE_SUMMARY.md](COVERAGE_SUMMARY.md)
- [REGRESSION_STATUS.md](REGRESSION_STATUS.md)
