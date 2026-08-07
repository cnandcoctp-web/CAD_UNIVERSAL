"""Annotation management for EvilTech CAD design context."""

from __future__ import annotations

from dataclasses import dataclass, field

from GEOMETRY.point import Point3D


@dataclass(slots=True)
class Annotation:
    """A user-authored design annotation."""

    identifier: str
    text: str
    anchor: Point3D
    tags: list[str] = field(default_factory=list)


class AnnotationManager:
    """Store and query annotations."""

    def __init__(self) -> None:
        self._annotations: dict[str, Annotation] = {}

    def add(self, annotation: Annotation) -> None:
        """Register an annotation."""
        self._annotations[annotation.identifier] = annotation

    def list_all(self) -> list[Annotation]:
        """Return all annotations."""
        return list(self._annotations.values())
