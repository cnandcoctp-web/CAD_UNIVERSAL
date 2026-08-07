"""Design metadata containers for EvilTech CAD."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DesignMetadata:
    """Serializable metadata about a design session."""

    author: str = ""
    revision: str = "A"
    tags: list[str] = field(default_factory=list)
    custom: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the metadata."""
        return {
            "author": self.author,
            "revision": self.revision,
            "tags": list(self.tags),
            "custom": dict(self.custom),
        }
