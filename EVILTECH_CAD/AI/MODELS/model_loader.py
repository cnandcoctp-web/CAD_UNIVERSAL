"""Model-loader helpers for the AI pipeline."""

from __future__ import annotations

from AI.MODELS.model_registry import ModelRegistry


class ModelLoader:
    """Return the in-process deterministic model registry."""

    def load(self) -> ModelRegistry:
        """Load the model registry."""
        return ModelRegistry()
