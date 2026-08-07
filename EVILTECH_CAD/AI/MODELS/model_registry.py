"""Registry of AI model components."""

from __future__ import annotations

from dataclasses import dataclass, field

from AI.MODELS.constraint_solver_model import ConstraintSolverModel
from AI.MODELS.design_quality_model import DesignQualityModel
from AI.MODELS.feature_recognition_model import FeatureRecognitionModel
from AI.MODELS.feedback_learning_model import FeedbackLearningModel
from AI.MODELS.geometry_model import GeometryModel
from AI.MODELS.manufacturability_model import ManufacturabilityModel


@dataclass(slots=True)
class ModelRegistry:
    """Bundle AI model components."""

    geometry_model: GeometryModel = field(default_factory=GeometryModel)
    feature_model: FeatureRecognitionModel = field(default_factory=FeatureRecognitionModel)
    manufacturability_model: ManufacturabilityModel = field(default_factory=ManufacturabilityModel)
    constraint_model: ConstraintSolverModel = field(default_factory=ConstraintSolverModel)
    quality_model: DesignQualityModel = field(default_factory=DesignQualityModel)
    feedback_model: FeedbackLearningModel = field(default_factory=FeedbackLearningModel)
