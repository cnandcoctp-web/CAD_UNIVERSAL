"""Conversation-state management for the AI Engineering Assistant."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class ConversationMessage:
    """A single user or assistant conversation message."""

    role: str
    content: str
    timestamp: str = field(default_factory=_utc_now)


@dataclass(slots=True)
class Conversation:
    """A named engineering conversation thread."""

    conversation_id: str
    discipline: str
    messages: list[ConversationMessage] = field(default_factory=list)
    created_at: str = field(default_factory=_utc_now)


class ConversationManager:
    """Manage AI assistant conversation threads."""

    def __init__(self) -> None:
        self._conversations: dict[str, Conversation] = {}

    def start_conversation(self, discipline: str) -> Conversation:
        """Start a new engineering conversation."""
        conversation = Conversation(conversation_id=str(uuid4()), discipline=discipline)
        self._conversations[conversation.conversation_id] = conversation
        return conversation

    def get(self, conversation_id: str) -> Conversation:
        """Return a conversation by identifier."""
        return self._conversations[conversation_id]

    def append_user_message(self, conversation_id: str, content: str) -> ConversationMessage:
        """Append a user message to a conversation."""
        return self._append(conversation_id, "user", content)

    def append_assistant_message(self, conversation_id: str, content: str) -> ConversationMessage:
        """Append an assistant message to a conversation."""
        return self._append(conversation_id, "assistant", content)

    def summarize(self, conversation_id: str) -> dict[str, object]:
        """Return a lightweight conversation summary."""
        conversation = self.get(conversation_id)
        latest = conversation.messages[-1].content if conversation.messages else ""
        return {
            "conversation_id": conversation.conversation_id,
            "discipline": conversation.discipline,
            "message_count": len(conversation.messages),
            "latest_message": latest,
        }

    def _append(self, conversation_id: str, role: str, content: str) -> ConversationMessage:
        conversation = self.get(conversation_id)
        message = ConversationMessage(role=role, content=content)
        conversation.messages.append(message)
        return message