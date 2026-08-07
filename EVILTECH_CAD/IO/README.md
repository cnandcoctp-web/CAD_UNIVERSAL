# Project Management And Persistence

The EvilTech CAD IO package provides the project management and data persistence
system for long-lived engineering projects. It integrates with locked packages
through approved public interfaces and keeps non-IO responsibilities out of the
module.

Implemented capabilities:

- Project manager and project creation wizard
- Project creation, loading, saving, and save-as flows
- Autosave, recovery, and backup management
- Project metadata, properties, version history, and file history
- Recent projects tracking
- Workspace persistence and session recovery state
- Asset registry and foundation resource-manager integration
- Project validation
- Import/export managers and file-format registry

Supported project storage layout:

- `project_metadata.json`
- `project_properties.json`
- `assets/`
- `materials/`
- `simulation_data/` placeholder
- `ai_history/` placeholder
- `configuration/`
- `logs/`
- `recovery/`
- `backups/`
- `versions/`

Not implemented here:

- Constraints, modeling, AI, simulation execution, or engineering domain modules
- Cloud synchronization and team collaboration backends beyond placeholder-ready configuration fields
