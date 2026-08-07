"""Regression and integration tests for the EvilTech CAD AI pipeline."""

from __future__ import annotations

from pathlib import Path

from AI.ai_controller import AIController
from AI.context_builder import ContextBuilder
from AI.context_manager import ContextManager
from AI.conversation_manager import ConversationManager
from AI.engineering_assistant import EngineeringAssistant
from AI.engineering_report_generator import EngineeringReportGenerator
from AI.knowledge_base import EngineeringKnowledgeBase
from AI.project_memory import ProjectMemory
from AI.prompt_manager import PromptManager
from AI.response_formatter import ResponseFormatter
from AI.FEEDBACK.design_feedback_parser import DesignFeedbackParser
from AI.FEEDBACK.feedback_registry import FeedbackRegistry
from AI.MODELS.model_manager import ModelManager
from AI.optimization_engine import OptimizationEngine
from AI.recommendation_engine import RecommendationEngine
from AI.SIGNALS.recommendation_exporter import RecommendationExporter
from AI.main import main as ai_main
from CONSTRAINTS.constraint_registry import ConstraintType
from CONSTRAINTS.constraint_solver import ConstraintManager
from GEOMETRY.line import Line
from GEOMETRY.point import Point3D
from IO.file_manager import ProjectManager
from MODELING.assembly import AssemblyManager, ComponentManager
from MODELING.feature import FeatureType
from MODELING.part import PartModel
from MODELING.sketch import SketchProfile


def build_part(name: str = "Analyzed Part", feature_count: int = 1) -> PartModel:
    part = PartModel(name=name)
    sketch = part.sketch_manager.create_sketch("Base", part.default_environment(), [SketchProfile(name="base", area=12.0, perimeter=14.0)])
    for index in range(feature_count):
        part.feature_manager.create_feature(FeatureType.EXTRUDE, f"Extrude-{index}", {"sketch": sketch.name, "distance": 2.0 + index})
    part.feature_manager.regenerate(part)
    return part


def test_ai_controller_processes_part_and_generates_recommendations() -> None:
    part = build_part(feature_count=14)
    controller = AIController()
    result = controller.process_part(part)

    assert result.report.snapshot.project_name == part.name
    assert result.geometry_state in {"concept", "developing", "detailed"}
    assert result.scorecard.overall_score() >= 0.0
    assert controller.performance_history.samples
    assert result.recommendations.routes


def test_engineering_assistant_maintains_conversation_and_context() -> None:
    part = build_part(feature_count=10)
    assistant = EngineeringAssistant()

    first = assistant.review_part(
        part,
        user_message="Review this bracket for manufacturability and constraint clarity.",
        discipline="mechanical_engineering",
    )
    second = assistant.review_part(
        part,
        user_message="Summarize the key risks again and explain the top recommendation.",
        discipline="manufacturing",
        conversation_id=first["conversation_id"],
    )

    assert first["conversation_id"] == second["conversation_id"]
    assert second["conversation_summary"]["message_count"] >= 2
    assert second["response"]["discipline"] == "manufacturing"
    assert second["response"]["recommendations"]


def test_context_builder_and_project_memory_capture_engineering_state(tmp_path: Path) -> None:
    project_manager = ProjectManager()
    snapshot = project_manager.create_new_project("AI Project", tmp_path / "ai_project")
    part = build_part(name="Memory Part", feature_count=4)
    context_builder = ContextBuilder()
    context = context_builder.build_for_part(part, project_snapshot=snapshot, discipline="structural_engineering")

    memory = ProjectMemory()
    memory.store_context(snapshot.metadata.project_id, context)
    stored = memory.get_context(snapshot.metadata.project_id)

    assert context.project_id == snapshot.metadata.project_id
    assert stored.discipline == "structural_engineering"
    assert stored.feature_count == 4


def test_knowledge_base_and_prompt_manager_cover_engineering_domains() -> None:
    knowledge_base = EngineeringKnowledgeBase()
    prompt_manager = PromptManager()
    model_manager = ModelManager()

    domains = knowledge_base.domain_names()
    prompt = prompt_manager.build_review_prompt(
        user_message="Suggest material and tolerance improvements.",
        discipline="material_science",
        context_summary="Precision shaft support bracket",
    )

    assert "mechanical_engineering" in domains
    assert "orbital_mechanics" in domains
    assert "fluid_mechanics" in domains
    assert "material_science" in prompt
    assert model_manager.model_names()


def test_recommendation_and_optimization_engines_produce_actionable_output() -> None:
    part = build_part(feature_count=18)
    result = AIController().process_part(part)
    recommendation_engine = RecommendationEngine()
    optimization_engine = OptimizationEngine()

    recommendations = recommendation_engine.rank(result.report, result.recommendations)
    plan = optimization_engine.build_plan(result.report, recommendations)

    assert recommendations
    assert plan["opportunities"]
    assert plan["estimated_impact"] >= 0.0


def test_engineering_report_generator_and_response_formatter_validate_responses() -> None:
    part = build_part(feature_count=8)
    result = AIController().process_part(part)
    report_generator = EngineeringReportGenerator()
    formatter = ResponseFormatter()

    report = report_generator.generate(result.report, result.scorecard, result.recommendations, discipline="civil_engineering")
    response = formatter.format_assistant_response(
        discipline="civil_engineering",
        report=report,
        recommendations=result.recommendations,
        explanation="The design is serviceable but feature complexity is increasing.",
    )

    assert report["discipline"] == "civil_engineering"
    assert report["recommendation_count"] == len(result.recommendations.recommendations)
    assert response["validated"] is True
    assert response["explanation"]


def test_ai_controller_includes_constraint_context() -> None:
    part = build_part(feature_count=3)
    manager = ConstraintManager()
    manager.add_entity("p1", Point3D(0.0, 0.0, 0.0))
    manager.add_entity("p2", Point3D(10.0, 0.0, 0.0))
    manager.add_constraint(ConstraintType.DISTANCE, ("p1", "p2"), value=10.0)
    result = AIController().process_part(part, constraints=manager)

    assert result.report.snapshot.constraint_summary["constraint_count"] == 1


def test_feedback_pipeline_updates_summary() -> None:
    registry = FeedbackRegistry()
    parser = DesignFeedbackParser()
    registry.add(parser.parse({"recommendation_id": "r1", "accepted": True, "rating": 5, "comments": "useful"}))
    registry.add(parser.parse({"recommendation_id": "r2", "accepted": False, "rating": 2}))

    summary = registry.summary()

    assert summary.total == 2
    assert summary.accepted == 1
    assert summary.average_rating == 3.5


def test_recommendation_exporter_writes_json(tmp_path: Path) -> None:
    part = build_part(feature_count=16)
    result = AIController().process_part(part)
    target = RecommendationExporter().export(result.recommendations, tmp_path / "recommendations.json")

    assert target.is_file()
    assert "recommendations" in target.read_text(encoding="utf-8")


def test_ai_main_returns_summary_payload() -> None:
    payload = ai_main()

    assert payload["findings"] >= 0
    assert payload["recommendations"] >= 0


def test_ai_supports_assembly_geometry_loading() -> None:
    component_manager = ComponentManager()
    assembly_manager = AssemblyManager(component_manager=component_manager)
    base = build_part("Base", feature_count=2)
    cap = build_part("Cap", feature_count=1)
    component_manager.add_component("base-1", base)
    component_manager.add_component("cap-1", cap)
    assembly = assembly_manager.create_assembly("Assembly")
    assembly_manager.add_to_assembly(assembly.name, "base-1")
    assembly_manager.add_to_assembly(assembly.name, "cap-1")

    dataset = AIController().data_registry.assemblies.load_assembly(assembly, component_manager)

    assert len(dataset.entities) == 2


def test_conversation_and_context_managers_scale_across_multiple_turns() -> None:
    conversation_manager = ConversationManager()
    context_manager = ContextManager()
    conversation = conversation_manager.start_conversation("manufacturing")
    for index in range(25):
        conversation_manager.append_user_message(conversation.conversation_id, f"Question {index}")
        conversation_manager.append_assistant_message(conversation.conversation_id, f"Answer {index}")
        context_manager.update_context(conversation.conversation_id, {"turn": index, "discipline": "manufacturing"})

    summary = conversation_manager.summarize(conversation.conversation_id)
    context = context_manager.get_context(conversation.conversation_id)

    assert summary["message_count"] == 50
    assert context["turn"] == 24


def test_end_to_end_engineering_project_workflow(tmp_path: Path) -> None:
    project_manager = ProjectManager()
    snapshot = project_manager.create_new_project("Engineering Workflow", tmp_path / "engineering_workflow")
    part = build_part(name="Workflow Part", feature_count=12)
    assistant = EngineeringAssistant()

    response = assistant.review_part(
        part,
        user_message="Create documentation-ready review guidance for this project.",
        discipline="architecture",
        project_snapshot=snapshot,
    )

    assert response["response"]["validated"] is True
    assert response["report"]["project_name"] == "Workflow Part"
    assert response["report"]["project_id"] == snapshot.metadata.project_id
    assert response["response"]["recommendations"]


def test_ai_pipeline_handles_dense_constraints_and_geometry() -> None:
    part = build_part(feature_count=20)
    manager = ConstraintManager()
    previous = Point3D(0.0, 0.0, 0.0)
    manager.add_entity("p0", previous)
    for index in range(1, 6):
        current = Point3D(float(index), 0.0, 0.0)
        manager.add_entity(f"p{index}", current)
        manager.add_entity(f"l{index}", Line(previous, current))
        manager.add_constraint(ConstraintType.DISTANCE, (f"p{index - 1}", f"p{index}"), value=1.0)
        previous = current

    result = AIController().process_part(part, constraints=manager)

    assert result.report.finding_count() >= 1
