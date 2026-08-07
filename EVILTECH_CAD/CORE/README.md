# Core Foundation

The `CORE` package contains the application runtime foundation for EvilTech CAD,
including configuration loading, lifecycle orchestration, project/session/workspace
management, logging, and shared service coordination. Higher-level packages build
on these services through explicit public interfaces rather than cross-package
state mutation.
