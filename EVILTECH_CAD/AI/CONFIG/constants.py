"""Constants used by the AI analysis pipeline."""

from __future__ import annotations

SEVERITIES = ("info", "warning", "critical")
PRIORITIES = ("low", "medium", "high")
ANALYSIS_CATEGORIES = (
    "geometry",
    "features",
    "manufacturability",
    "constraints",
    "tolerances",
    "anomaly",
)
