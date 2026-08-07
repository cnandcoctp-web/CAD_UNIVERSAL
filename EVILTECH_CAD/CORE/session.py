"""Session management for the EvilTech CAD foundation layer.

Sessions represent an active user context and are kept lightweight so that the
foundation can support later multi-session and multi-user workflows.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional
from uuid import uuid4

from CORE.constants import LifecycleState
from CORE.exceptions import SessionError


@dataclass(slots=True)
class Session:
    """A lightweight user session record."""

    id: str
    user_id: str
    state: LifecycleState = LifecycleState.ACTIVE
    metadata: Dict[str, str] = field(default_factory=dict)


class SessionManager:
    """Create and manage active user sessions."""

    def __init__(self) -> None:
        """Initialize the session manager."""
        self._sessions: Dict[str, Session] = {}

    def create_session(self, user_id: str, metadata: Optional[Dict[str, str]] = None) -> Session:
        """Create a new active session.

        Args:
            user_id: The user identifier.
            metadata: Optional metadata to attach to the session.

        Returns:
            The created session.

        Raises:
            SessionError: If the user identifier is invalid.
        """
        if not user_id or not user_id.strip():
            raise SessionError("User identifier must be non-empty.")
        session = Session(id=str(uuid4()), user_id=user_id.strip(), metadata=dict(metadata or {}))
        self._sessions[session.id] = session
        return session

    def close_session(self, session_id: str) -> Session:
        """Close an existing session.

        Args:
            session_id: The session identifier.

        Returns:
            The updated session.

        Raises:
            SessionError: If the session is not found.
        """
        session = self._sessions.get(session_id)
        if session is None:
            raise SessionError(f"Session '{session_id}' does not exist.")
        session.state = LifecycleState.CLOSED
        return session

    def get_session(self, session_id: str) -> Session:
        """Retrieve a session by identifier."""
        session = self._sessions.get(session_id)
        if session is None:
            raise SessionError(f"Session '{session_id}' does not exist.")
        return session
