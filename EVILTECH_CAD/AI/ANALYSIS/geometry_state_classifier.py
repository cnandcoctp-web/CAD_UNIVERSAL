"""Geometry-state classification for the AI pipeline."""

from __future__ import annotations

from AI.SCHEMAS.analysis_schema import DesignSnapshot


class GeometryStateClassifier:
    """Classify the maturity of a design from geometry metrics."""

    def classify(self, snapshot: DesignSnapshot) -> str:
        """Return a geometry maturity label."""
        face_count = snapshot.geometry.total_faces()
        if face_count < 10:
            return "concept"
        if face_count < 30:
            return "developing"
        return "detailed"
