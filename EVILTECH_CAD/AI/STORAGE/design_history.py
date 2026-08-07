"""AI-visible design snapshot history."""

from __future__ import annotations

from dataclasses import dataclass, field

from AI.SCHEMAS.analysis_schema import DesignSnapshot


@dataclass(slots=True)
class AIDesignHistory:
    """Store analyzed design snapshots."""

    snapshots: list[DesignSnapshot] = field(default_factory=list)

    def record(self, snapshot: DesignSnapshot) -> None:
        """Record a design snapshot."""
        self.snapshots.append(snapshot)
