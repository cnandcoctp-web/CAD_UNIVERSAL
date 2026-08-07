"""Boolean body operations for the modeling engine."""

from __future__ import annotations

from MODELING.body import ModelBody


class BooleanOperation:
    """Apply lightweight boolean operations to model bodies."""

    @staticmethod
    def apply(operation: str, left: ModelBody, right: ModelBody) -> ModelBody:
        """Apply a boolean operation and return the resulting body."""
        if operation == "union":
            return ModelBody(name=f"{left.name}-union", volume=left.volume + right.volume, face_count=left.face_count + right.face_count, edge_count=left.edge_count + right.edge_count, body_count=max(left.body_count, right.body_count))
        if operation == "subtract":
            return ModelBody(name=f"{left.name}-subtract", volume=max(0.0, left.volume - right.volume), face_count=max(1, left.face_count), edge_count=max(1, left.edge_count), body_count=left.body_count)
        if operation == "intersect":
            return ModelBody(name=f"{left.name}-intersect", volume=min(left.volume, right.volume), face_count=min(left.face_count, right.face_count), edge_count=min(left.edge_count, right.edge_count), body_count=1)
        raise ValueError(f"Unsupported boolean operation '{operation}'")
