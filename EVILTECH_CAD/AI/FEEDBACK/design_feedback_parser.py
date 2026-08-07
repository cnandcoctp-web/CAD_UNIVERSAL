"""Feedback parsing helpers for the AI pipeline."""

from __future__ import annotations

from AI.SCHEMAS.feedback_schema import FeedbackRecord


class DesignFeedbackParser:
    """Parse simple mapping payloads into feedback records."""

    def parse(self, payload: dict[str, object]) -> FeedbackRecord:
        """Parse a feedback payload."""
        return FeedbackRecord(
            recommendation_id=str(payload["recommendation_id"]),
            accepted=bool(payload.get("accepted", False)),
            rating=int(payload.get("rating", 0)),
            comments=str(payload.get("comments", "")),
            tags=[str(tag) for tag in payload.get("tags", [])],
        )
