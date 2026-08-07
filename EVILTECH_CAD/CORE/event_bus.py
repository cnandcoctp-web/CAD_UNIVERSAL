"""Event bus for the EvilTech CAD foundation layer.

The event bus provides a simple, typed, and defensive mechanism for
publish-subscribe communication between the application foundation services.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional
from uuid import uuid4

from CORE.exceptions import EventBusError


@dataclass(slots=True)
class EventEnvelope:
    """A serializable event envelope for foundation communication."""

    event_type: str
    payload: Dict[str, Any] = field(default_factory=dict)
    source: str = "foundation"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_id: str = field(default_factory=lambda: str(uuid4()))


class EventBus:
    """Publish and subscribe to typed application events."""

    def __init__(self) -> None:
        """Initialize the event bus with an empty subscription registry."""
        self._subscriptions: Dict[str, List[Callable[[EventEnvelope], None]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[EventEnvelope], None]) -> None:
        """Register a handler for a specific event type.

        Args:
            event_type: The event type name.
            handler: The callback to invoke for matching events.

        Raises:
            EventBusError: If the event type or handler is invalid.
        """
        if not event_type or not event_type.strip():
            raise EventBusError("Event type must be non-empty.")
        if not callable(handler):
            raise EventBusError("Event handler must be callable.")
        self._subscriptions.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, payload: Optional[Dict[str, Any]] = None, source: str = "foundation") -> EventEnvelope:
        """Publish an event to all registered subscribers.

        Args:
            event_type: The event type name.
            payload: Optional structured payload for the event.
            source: The component emitting the event.

        Returns:
            The emitted event envelope.

        Raises:
            EventBusError: If the event type is invalid.
        """
        if not event_type or not event_type.strip():
            raise EventBusError("Event type must be non-empty.")
        envelope = EventEnvelope(event_type=event_type, payload=payload or {}, source=source)
        for handler in list(self._subscriptions.get(event_type, [])):
            handler(envelope)
        return envelope

    def clear(self) -> None:
        """Remove all registered subscriptions."""
        self._subscriptions.clear()
