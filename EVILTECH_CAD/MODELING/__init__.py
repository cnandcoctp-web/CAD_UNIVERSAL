"""Parametric modeling engine package for EvilTech CAD."""

from MODELING.assembly import AssemblyManager, ComponentManager, Mate, PartManager
from MODELING.boolean import BooleanOperation
from MODELING.feature import (
    DesignHistory,
    Feature,
    FeatureManager,
    FeatureTree,
    FeatureType,
    ModelBody,
    ParametricHistory,
    ReferenceGeometry,
    RegenerationResult,
    WorkAxis,
    WorkPlane,
    WorkPoint,
)
from MODELING.part import PartModel
from MODELING.sketch import Sketch, SketchEnvironment, SketchManager, SketchProfile, SketchValidationResult, SketchValidator

__all__ = [
    "AssemblyManager",
    "BooleanOperation",
    "ComponentManager",
    "DesignHistory",
    "Feature",
    "FeatureManager",
    "FeatureTree",
    "FeatureType",
    "Mate",
    "ModelBody",
    "ParametricHistory",
    "PartManager",
    "PartModel",
    "ReferenceGeometry",
    "RegenerationResult",
    "Sketch",
    "SketchEnvironment",
    "SketchManager",
    "SketchProfile",
    "SketchValidationResult",
    "SketchValidator",
    "WorkAxis",
    "WorkPlane",
    "WorkPoint",
]