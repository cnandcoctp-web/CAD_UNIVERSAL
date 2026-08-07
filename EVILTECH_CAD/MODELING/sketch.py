"""Sketch management for the modeling engine."""

from __future__ import annotations

from dataclasses import dataclass, field

from MODELING.feature import ReferenceGeometry, WorkAxis, WorkPlane, WorkPoint


@dataclass(slots=True)
class SketchProfile:
    """A simplified sketch profile used for feature creation."""

    name: str
    area: float
    perimeter: float
    closed: bool = True


@dataclass(slots=True)
class SketchEnvironment:
    """Sketch working environment and references."""

    work_plane: WorkPlane
    work_axis: WorkAxis
    work_point: WorkPoint
    references: list[ReferenceGeometry] = field(default_factory=list)


@dataclass(slots=True)
class Sketch:
    """A named sketch containing one or more profiles."""

    name: str
    environment: SketchEnvironment
    profiles: list[SketchProfile] = field(default_factory=list)

    def profile_count(self) -> int:
        """Return the number of profiles in the sketch."""
        return len(self.profiles)


@dataclass(slots=True)
class SketchValidationResult:
    """Validation result for a sketch."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)


class SketchValidator:
    """Validate sketch profiles before feature creation."""

    def validate(self, sketch: Sketch) -> SketchValidationResult:
        """Validate a sketch and its profiles."""
        errors: list[str] = []
        if not sketch.name:
            errors.append("Sketch name must be non-empty")
        if not sketch.profiles:
            errors.append("Sketch must contain at least one profile")
        for profile in sketch.profiles:
            if not profile.closed:
                errors.append(f"Profile '{profile.name}' must be closed")
            if profile.area <= 0.0:
                errors.append(f"Profile '{profile.name}' must have positive area")
        return SketchValidationResult(is_valid=not errors, errors=errors)


class SketchManager:
    """Create and manage sketches for a part model."""

    def __init__(self) -> None:
        self._sketches: dict[str, Sketch] = {}

    def create_sketch(self, name: str, environment: SketchEnvironment, profiles: list[SketchProfile]) -> Sketch:
        """Create and register a sketch."""
        sketch = Sketch(name=name, environment=environment, profiles=list(profiles))
        validation = SketchValidator().validate(sketch)
        if not validation.is_valid:
            raise ValueError("Invalid sketch: " + "; ".join(validation.errors))
        self._sketches[name] = sketch
        return sketch

    def get(self, name: str) -> Sketch:
        """Return a sketch by name."""
        return self._sketches[name]
