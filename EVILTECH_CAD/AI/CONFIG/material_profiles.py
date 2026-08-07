"""Material-specific AI heuristics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MaterialProfile:
    """AI-facing material process profile."""

    key: str
    machining_score: float
    additive_score: float
    stiffness_score: float


DEFAULT_MATERIAL_PROFILES: dict[str, MaterialProfile] = {
    "aluminum-6061": MaterialProfile("aluminum-6061", machining_score=0.9, additive_score=0.5, stiffness_score=0.7),
    "steel-1018": MaterialProfile("steel-1018", machining_score=0.75, additive_score=0.2, stiffness_score=0.9),
    "abs": MaterialProfile("abs", machining_score=0.3, additive_score=0.95, stiffness_score=0.35),
    "titanium-ti6al4v": MaterialProfile("titanium-ti6al4v", machining_score=0.35, additive_score=0.7, stiffness_score=0.95),
}
