"""Feedback schema definitions for the AI pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FeedbackRecord:
    """A user response to a recommendation."""

    recommendation_id: str
    accepted: bool
    rating: int = 0
    comments: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass(slots=True)
class FeedbackSummary:
    """Summary statistics across feedback records."""

    total: int
    accepted: int
    average_rating: float
