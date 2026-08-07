# Industrial CAD Gap Analysis

## Assessment Basis

This gap analysis compares the current EVILTECH CAD repository architecture against the class of systems represented by Siemens NX, CATIA, SolidWorks, Creo, Fusion 360, FreeCAD, and OpenCascade-based platforms.

The ranking is by architectural importance.

## Tier 1: Highest-Impact Missing Capabilities

1. Real B-Rep kernel boundary
   - EVILTECH CAD currently has primitive geometry and lightweight body summaries, not a production topology kernel.
2. Persistent topological naming
   - No stable face, edge, loop, vertex, or sketch entity identity survives regeneration.
3. Kernel-based history modeling
   - Feature execution is arithmetic replay, not journaled kernel transactions.
4. Industrial assembly persistence
   - Current JSON persistence is insufficient for very large product structures and partial loading.
5. Solver SPI with typed problem definitions
   - The simulation layer is orchestration only.

## Tier 2: Core Platform Gaps

6. GPU rendering backend abstraction
7. Tessellation and display-mesh pipeline
8. Assembly-scale change propagation and selective regeneration
9. Sketch/3D/assembly constraint architecture separation
10. Plugin-based engineering discipline extensibility

## Tier 3: Product Ecosystem Gaps

11. PMI/MBD and drawing architecture
12. Manufacturing/CAM architecture
13. enterprise metadata, PLM, and workflow integration
14. collaboration and branching/merge of design state
15. public scripting and automation SDK

## Comparative Notes

- Siemens NX / CATIA / Creo
  - EVILTECH CAD is far behind in kernel infrastructure, topology resilience, assemblies, persistence, simulation coupling, and enterprise integration.
- SolidWorks / Fusion 360
  - EVILTECH CAD is behind in workflow completeness, plugin ecosystem, and usable production modeling depth.
- FreeCAD / OpenCascade
  - EVILTECH CAD is behind in foundational geometry-kernel maturity.

## Brutally Honest Summary

The current repository is a strong deterministic prototype and architectural testbed. It is not yet a production CAD platform. Its biggest limitation is not UI polish or missing commands; it is the lack of an industrial kernel-centered architecture.

## Recommendation

Do not treat Version 2.0 as a feature-release cycle. Treat it as a platform-architecture cycle focused on kernel boundaries, topology persistence, rendering backend abstraction, solver SPI, and industrial persistence.