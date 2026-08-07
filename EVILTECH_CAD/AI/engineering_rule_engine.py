"""Engineering rule validation for the AI Engineering Assistant."""

from __future__ import annotations

from AI.knowledge_base import EngineeringKnowledgeBase


class EngineeringRuleEngine:
    """Enforce architectural and response constraints for the assistant."""

    FORBIDDEN_CONTROL_TERMS = ("click", "press the button", "execute automatically", "control the application")

    def __init__(self, knowledge_base: EngineeringKnowledgeBase | None = None) -> None:
        self.knowledge_base = knowledge_base or EngineeringKnowledgeBase()

    def validate_discipline(self, discipline: str) -> None:
        """Ensure the requested discipline is supported."""
        if discipline not in self.knowledge_base.domain_names():
            raise ValueError(f"Unsupported engineering discipline '{discipline}'")

    def validate_response(self, response: dict[str, object]) -> bool:
        """Validate an assistant response payload."""
        explanation = str(response.get("explanation", "")).lower()
        if any(term in explanation for term in self.FORBIDDEN_CONTROL_TERMS):
            raise ValueError("Assistant responses must analyze and recommend without controlling the application")
        return True