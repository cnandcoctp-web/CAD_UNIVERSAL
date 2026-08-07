"""AI integration helpers for engineering disciplines."""

from __future__ import annotations

from AI.engineering_assistant import EngineeringAssistant

from ENGINEERING.engineering_models import DisciplineType


class EngineeringAIIntegration:
    """Build AI-facing review payloads for engineering modules."""

    def build_review_payload(self, assistant: EngineeringAssistant, discipline: DisciplineType, context_summary: str) -> dict[str, object]:
        """Build an AI review payload using the shared engineering assistant."""
        domain = assistant.knowledge_base.get_domain(discipline.value)
        return {
            "discipline": discipline.value,
            "context_summary": context_summary,
            "domain_summary": domain.summary,
            "future_integrations": assistant.knowledge_base.future_integrations(),
        }