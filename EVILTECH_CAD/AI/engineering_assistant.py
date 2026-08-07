"""High-level engineering assistant for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass, field

from AI.ai_controller import AIController
from AI.context_builder import ContextBuilder
from AI.context_manager import ContextManager
from AI.conversation_manager import ConversationManager
from AI.engineering_report_generator import EngineeringReportGenerator
from AI.engineering_rule_engine import EngineeringRuleEngine
from AI.knowledge_base import EngineeringKnowledgeBase
from AI.optimization_engine import OptimizationEngine
from AI.project_memory import ProjectMemory
from AI.prompt_manager import PromptManager
from AI.recommendation_engine import RecommendationEngine
from AI.response_formatter import ResponseFormatter


@dataclass(slots=True)
class EngineeringAssistant:
    """User-facing engineering assistant that explains and recommends."""

    controller: AIController = field(default_factory=AIController)
    conversations: ConversationManager = field(default_factory=ConversationManager)
    contexts: ContextManager = field(default_factory=ContextManager)
    memory: ProjectMemory = field(default_factory=ProjectMemory)
    knowledge_base: EngineeringKnowledgeBase = field(default_factory=EngineeringKnowledgeBase)
    rules: EngineeringRuleEngine = field(default_factory=EngineeringRuleEngine)
    prompts: PromptManager = field(default_factory=PromptManager)
    recommender: RecommendationEngine = field(default_factory=RecommendationEngine)
    optimizer: OptimizationEngine = field(default_factory=OptimizationEngine)
    formatter: ResponseFormatter = field(default_factory=ResponseFormatter)
    reports: EngineeringReportGenerator = field(default_factory=EngineeringReportGenerator)
    context_builder: ContextBuilder = field(default_factory=ContextBuilder)

    def review_part(
        self,
        part,
        user_message: str,
        discipline: str,
        conversation_id: str | None = None,
        project_snapshot=None,
        constraints=None,
        material_key: str = "aluminum-6061",
    ) -> dict[str, object]:
        """Review a part and return an assistant response bundle."""
        self.rules.validate_discipline(discipline)
        conversation = self.conversations.start_conversation(discipline) if conversation_id is None else self.conversations.get(conversation_id)
        self.conversations.append_user_message(conversation.conversation_id, user_message)

        context = self.context_builder.build_for_part(part, project_snapshot=project_snapshot, discipline=discipline, material_key=material_key)
        self.contexts.update_context(
            conversation.conversation_id,
            {
                "discipline": discipline,
                "project_name": context.project_name,
                "feature_count": context.feature_count,
                "project_id": context.project_id,
            },
        )
        if context.project_id is not None:
            self.memory.store_context(context.project_id, context)

        summary = self.knowledge_base.get_domain(discipline).summary
        prompt = self.prompts.build_review_prompt(user_message=user_message, discipline=discipline, context_summary=summary)
        result = self.controller.process_part(part, constraints=constraints, material_key=material_key)
        ranked = self.recommender.rank(result.report, result.recommendations)
        optimization_plan = self.optimizer.build_plan(result.report, ranked)
        report = self.reports.generate(
            result.report,
            result.scorecard,
            result.recommendations,
            discipline=discipline,
            project_id=context.project_id,
        )
        explanation = self._build_explanation(result.report.finding_count(), ranked, prompt)
        response = self.formatter.format_assistant_response(
            discipline=discipline,
            report=report,
            recommendations=result.recommendations,
            explanation=explanation,
        )
        self.conversations.append_assistant_message(conversation.conversation_id, explanation)
        if context.project_id is not None:
            self.memory.store_report(context.project_id, report)
        return {
            "conversation_id": conversation.conversation_id,
            "conversation_summary": self.conversations.summarize(conversation.conversation_id),
            "context": self.contexts.get_context(conversation.conversation_id),
            "prompt": prompt,
            "report": report,
            "response": response,
            "optimization_plan": optimization_plan,
        }

    @staticmethod
    def _build_explanation(finding_count: int, ranked_recommendations, prompt: str) -> str:
        top = ranked_recommendations[0].title if ranked_recommendations else "No critical recommendation"
        return f"Analyzed the design without controlling the application. Findings: {finding_count}. Top recommendation: {top}. Prompt basis: {prompt}"