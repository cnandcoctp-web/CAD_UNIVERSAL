# Constraint Engine

The EvilTech CAD constraint engine provides a modular, headless parametric
constraint solver for sketch-style engineering geometry. It integrates with the
locked Foundation, Mathematical Engine, Geometry Kernel, Rendering Engine, User
Interface, and Project System through public interfaces only.

Implemented capabilities:

- Constraint manager, registry, solver, validator, dependency graph, history
- Constraint persistence and event tracking
- Conflict detection, simple conflict resolution, incremental solving
- Undo and redo for solver state changes
- Supported constraint types: coincident, parallel, perpendicular, horizontal,
  vertical, distance, angle, radius, diameter, concentric, tangent,
  equal length, equal radius, symmetry, midpoint, offset, lock, reference,
  driving, and driven

Current scope:

- Headless 2D-style geometric solving over points, lines, and circles
- Placeholder-ready architecture for later modeling and larger engineering workflows
