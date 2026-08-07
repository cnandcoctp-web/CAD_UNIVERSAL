"""Recommendation schema definitions for the AI pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Recommendation:
    """A user-facing design recommendation."""

    identifier: str
    category: str
    title: str
    description: str
    priority: str
    confidence: float
    actions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RecommendationBundle:
    """Collection of recommendations grouped by route."""

    recommendations: list[Recommendation] = field(default_factory=list)
    routes: dict[str, list[str]] = field(default_factory=dict)
