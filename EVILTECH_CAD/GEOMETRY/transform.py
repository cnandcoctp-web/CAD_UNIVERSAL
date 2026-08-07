"""Geometric transformation helpers for the EvilTech CAD geometry kernel."""

from __future__ import annotations

from dataclasses import dataclass

from MATH_ENGINE.transforms import Transform as MathTransform


@dataclass(slots=True)
class GeometricTransform:
    """A thin wrapper exposing the approved math-engine transform constructors."""

    transform: MathTransform

    def __post_init__(self) -> None:
        """Validate the wrapped transform."""
        if not isinstance(self.transform, MathTransform):
            raise TypeError("transform must be a MathTransform instance")

    @classmethod
    def translation(cls, tx: float, ty: float, tz: float) -> "GeometricTransform":
        """Create a translation transform."""
        return cls(MathTransform.translation(tx, ty, tz))

    @classmethod
    def rotation_z(cls, angle: float) -> "GeometricTransform":
        """Create a z-axis rotation transform."""
        return cls(MathTransform.rotation_z(angle))

    @classmethod
    def scale(cls, sx: float, sy: float, sz: float) -> "GeometricTransform":
        """Create a scale transform."""
        return cls(MathTransform.scale(sx, sy, sz))

    def to_dict(self) -> dict[str, object]:
        """Serialize the transform wrapper to a dictionary."""
        return {"type": "geometric_transform"}
