# Known Issues Report

## Minor Issues

- Editor diagnostics in this environment report unresolved `pytest` imports in some test files despite successful execution in the configured runtime.
- The shared terminal wrapper can move completed long-running commands to the background after printing successful output.
- `/usr/bin/time` is not present in this container, so timing metrics were collected with Python runtime instrumentation instead.

## Critical Issues

- None identified.

## Release Impact

- None of the listed minor issues block build, launch, regression execution, or the end-to-end engineering workflow.
