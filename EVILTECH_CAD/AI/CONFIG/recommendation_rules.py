"""Templates and routing rules for AI recommendations."""

from __future__ import annotations

RULE_TEMPLATES: dict[str, dict[str, object]] = {
    "manufacturability": {
        "title": "Improve Manufacturability",
        "actions": ["Reduce thin features", "Prefer stock-friendly dimensions", "Review process selection"],
        "route": "manufacturing",
    },
    "constraints": {
        "title": "Review Constraint Stability",
        "actions": ["Inspect conflicting constraints", "Lock reference geometry", "Reduce redundant dimensions"],
        "route": "constraints",
    },
    "anomaly": {
        "title": "Investigate Unusual Geometry",
        "actions": ["Review recent feature edits", "Compare against prior design baseline"],
        "route": "modeling",
    },
    "tolerances": {
        "title": "Adjust Tolerance Strategy",
        "actions": ["Relax non-critical tolerances", "Apply standards-based limits"],
        "route": "documentation",
    },
    "features": {
        "title": "Simplify Feature Stack",
        "actions": ["Merge patterned operations", "Suppress non-essential detail for early iterations"],
        "route": "modeling",
    },
    "geometry": {
        "title": "Review Geometry Complexity",
        "actions": ["Reduce face count", "Replace complex lofts with simpler profiles where possible"],
        "route": "modeling",
    },
}
