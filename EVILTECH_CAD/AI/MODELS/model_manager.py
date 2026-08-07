"""Model access management for the AI Engineering Assistant."""

from __future__ import annotations

from AI.MODELS.model_loader import ModelLoader


class ModelManager:
    """Expose loaded deterministic AI models."""

    def __init__(self, loader: ModelLoader | None = None) -> None:
        self.loader = loader or ModelLoader()

    def model_names(self) -> list[str]:
        """Return the registered deterministic model names."""
        registry = self.loader.load()
        return [
            registry.geometry_model.__class__.__name__,
            registry.feature_model.__class__.__name__,
            registry.manufacturability_model.__class__.__name__,
            registry.constraint_model.__class__.__name__,
            registry.quality_model.__class__.__name__,
            registry.feedback_model.__class__.__name__,
        ]