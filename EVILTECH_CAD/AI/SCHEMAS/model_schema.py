"""Model evaluation schema definitions for the AI pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ModelEvaluation:
    """Standardized output from an AI model component."""

    model_name: str
    score: float
    confidence: float
    signals: dict[str, Any] = field(default_factory=dict)
