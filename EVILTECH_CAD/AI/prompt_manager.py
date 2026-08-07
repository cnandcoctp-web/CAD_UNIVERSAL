"""Prompt construction for the AI Engineering Assistant."""

from __future__ import annotations


class PromptManager:
    """Build deterministic prompts from engineering intent and context."""

    def build_review_prompt(self, user_message: str, discipline: str, context_summary: str) -> str:
        """Build a review prompt for the engineering assistant."""
        return (
            f"Discipline: {discipline}\n"
            f"Task: Analyze, explain, recommend, and optimize without controlling the application.\n"
            f"Context: {context_summary}\n"
            f"User request: {user_message}"
        )