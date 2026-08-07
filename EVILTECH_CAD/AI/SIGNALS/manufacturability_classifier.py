"""Manufacturability signal classification."""

from __future__ import annotations


class ManufacturabilityClassifier:
    """Map manufacturability scores to status labels."""

    def classify(self, score: float) -> str:
        """Return a manufacturability label."""
        if score >= 0.75:
            return "strong"
        if score >= 0.45:
            return "moderate"
        return "weak"
