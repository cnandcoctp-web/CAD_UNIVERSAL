"""Context-state management for the AI Engineering Assistant."""

from __future__ import annotations


class ContextManager:
    """Store mutable per-conversation context for assistant turns."""

    def __init__(self) -> None:
        self._contexts: dict[str, dict[str, object]] = {}

    def update_context(self, conversation_id: str, payload: dict[str, object]) -> dict[str, object]:
        """Merge new context values into the active conversation context."""
        context = self._contexts.setdefault(conversation_id, {})
        context.update(payload)
        return dict(context)

    def get_context(self, conversation_id: str) -> dict[str, object]:
        """Return the stored conversation context."""
        return dict(self._contexts.get(conversation_id, {}))