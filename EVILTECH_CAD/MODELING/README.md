# Modeling Engine

The EvilTech CAD modeling module provides a headless parametric feature-based
modeling engine with lightweight body math, feature regeneration, history, and
assembly management.

Implemented capabilities:

- Sketch manager, sketch environment, and sketch validator
- Feature manager, feature tree, parametric history, and design history
- Reference geometry, work planes, work axes, and work points
- Parametric feature regeneration with undo, redo, suppression, rollback,
	editing, dependency metadata, and automatic rebuild
- Headless assembly managers with components, mates, exploded views, and
	assembly tree support

Current scope:

- Lightweight feature-volume/body representation rather than a full B-rep kernel
- Deterministic parametric rebuild behavior for early engineering workflows
