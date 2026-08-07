"""Feedback storage for the AI pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field

from AI.SCHEMAS.feedback_schema import FeedbackRecord, FeedbackSummary


@dataclass(slots=True)
class FeedbackRegistry:
    """Store recommendation feedback records."""

    records: list[FeedbackRecord] = field(default_factory=list)

    def add(self, record: FeedbackRecord) -> None:
        """Store a feedback record."""
        self.records.append(record)

    def summary(self) -> FeedbackSummary:
        """Return aggregate feedback statistics."""
        total = len(self.records)
        accepted = sum(1 for record in self.records if record.accepted)
        average_rating = sum(record.rating for record in self.records) / total if total else 0.0
        return FeedbackSummary(total=total, accepted=accepted, average_rating=average_rating)
