"""Entry point for the EvilTech CAD deterministic AI pipeline."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from AI.engineering_assistant import EngineeringAssistant
from MODELING.feature import FeatureType
from MODELING.part import PartModel
from MODELING.sketch import SketchProfile


def build_demo_part() -> PartModel:
    """Build a small demo part for standalone AI execution."""
    part = PartModel(name="AI Demo Part")
    sketch = part.sketch_manager.create_sketch("Base", part.default_environment(), [SketchProfile(name="base", area=10.0, perimeter=14.0)])
    part.feature_manager.create_feature(FeatureType.EXTRUDE, "Extrude", {"sketch": sketch.name, "distance": 4.0})
    part.feature_manager.regenerate(part)
    return part


def main() -> dict[str, object]:
    """Execute the AI pipeline on a demo part and return a summary."""
    assistant = EngineeringAssistant()
    review = assistant.review_part(
        build_demo_part(),
        user_message="Review this part for engineering quality and recommendations.",
        discipline="mechanical_engineering",
    )
    report = review["report"]
    response = review["response"]
    return {
        "findings": report["finding_count"],
        "recommendations": len(response["recommendations"]),
        "geometry_state": review["context"]["discipline"],
        "overall_score": round(float(report["overall_score"]), 3),
    }


if __name__ == "__main__":
    print(main())
