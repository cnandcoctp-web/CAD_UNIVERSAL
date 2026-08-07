"""Camera systems and controllers for the EvilTech CAD rendering engine."""

from __future__ import annotations

import math
from dataclasses import dataclass

from GEOMETRY.point import Point3D
from GEOMETRY.vector import Vector3D


def _ensure_point(value: Point3D, name: str) -> None:
    if not isinstance(value, Point3D):
        raise TypeError(f"{name} must be a Point3D")


def _ensure_vector(value: Vector3D, name: str) -> None:
    if not isinstance(value, Vector3D):
        raise TypeError(f"{name} must be a Vector3D")


@dataclass(slots=True)
class BaseCamera:
    """Shared camera state for 2D and 3D workspaces."""

    position: Point3D
    target: Point3D
    up: Vector3D

    def __post_init__(self) -> None:
        _ensure_point(self.position, "position")
        _ensure_point(self.target, "target")
        _ensure_vector(self.up, "up")
        if self.up.magnitude() == 0.0:
            raise ValueError("up vector must be non-zero")

    def view_direction(self) -> Vector3D:
        """Return the normalized view direction from position to target."""
        delta = Vector3D(self.target.x - self.position.x, self.target.y - self.position.y, self.target.z - self.position.z)
        return delta.normalized()

    def move(self, delta: Vector3D) -> None:
        """Translate the camera position and target by the same delta."""
        _ensure_vector(delta, "delta")
        self.position = self.position.translate(delta)
        self.target = self.target.translate(delta)


@dataclass(slots=True)
class PerspectiveCamera(BaseCamera):
    """Perspective camera definition for 3D rendering."""

    field_of_view: float
    aspect_ratio: float
    near_clip: float = 0.1
    far_clip: float = 1000.0

    def __post_init__(self) -> None:
        BaseCamera.__post_init__(self)
        if self.field_of_view <= 0.0 or self.field_of_view >= 180.0:
            raise ValueError("field_of_view must be within (0, 180)")
        if self.aspect_ratio <= 0.0:
            raise ValueError("aspect_ratio must be positive")

    def projection_state(self) -> dict[str, float]:
        """Return serializable perspective projection parameters."""
        return {
            "type": "perspective",
            "field_of_view": self.field_of_view,
            "aspect_ratio": self.aspect_ratio,
            "near_clip": self.near_clip,
            "far_clip": self.far_clip,
        }

    def resize(self, width: float, height: float) -> None:
        """Update the aspect ratio to match the viewport size."""
        if width <= 0.0 or height <= 0.0:
            raise ValueError("width and height must be positive")
        self.aspect_ratio = width / height


@dataclass(slots=True)
class OrthographicCamera(BaseCamera):
    """Orthographic camera definition for 2D and drafting views."""

    width: float
    height: float
    near_clip: float = -1000.0
    far_clip: float = 1000.0

    def __post_init__(self) -> None:
        BaseCamera.__post_init__(self)
        if self.width <= 0.0 or self.height <= 0.0:
            raise ValueError("width and height must be positive")

    def resize(self, width: float, height: float) -> None:
        """Resize the orthographic projection extents."""
        if width <= 0.0 or height <= 0.0:
            raise ValueError("width and height must be positive")
        self.width = width
        self.height = height

    def projection_state(self) -> dict[str, float]:
        """Return serializable orthographic projection parameters."""
        return {
            "type": "orthographic",
            "width": self.width,
            "height": self.height,
            "near_clip": self.near_clip,
            "far_clip": self.far_clip,
        }


class CameraController:
    """High-level camera manipulation for zoom, pan, orbit, and rotate."""

    def __init__(self, camera: BaseCamera) -> None:
        if not isinstance(camera, BaseCamera):
            raise TypeError("camera must be a BaseCamera")
        self.camera = camera

    def view_direction(self) -> Vector3D:
        """Return the current normalized view direction."""
        return self.camera.view_direction()

    def zoom(self, delta: float) -> None:
        """Move the camera along its view direction."""
        if not isinstance(delta, (int, float)):
            raise TypeError("delta must be numeric")
        direction = self.camera.view_direction()
        self.camera.position = self.camera.position.translate(direction * float(delta))

    def pan(self, delta_x: float, delta_y: float) -> None:
        """Translate the camera parallel to the view plane."""
        if not isinstance(delta_x, (int, float)) or not isinstance(delta_y, (int, float)):
            raise TypeError("pan deltas must be numeric")
        delta = Vector3D(float(delta_x), float(delta_y), 0.0)
        self.camera.move(delta)

    def rotate(self, yaw_degrees: float, pitch_degrees: float) -> None:
        """Rotate the camera position around the target."""
        self._orbit(yaw_degrees, pitch_degrees)

    def orbit(self, yaw_degrees: float, pitch_degrees: float) -> None:
        """Orbit the camera around the target."""
        self._orbit(yaw_degrees, pitch_degrees)

    def _orbit(self, yaw_degrees: float, pitch_degrees: float) -> None:
        if not isinstance(yaw_degrees, (int, float)) or not isinstance(pitch_degrees, (int, float)):
            raise TypeError("orbit angles must be numeric")
        offset = Vector3D(
            self.camera.position.x - self.camera.target.x,
            self.camera.position.y - self.camera.target.y,
            self.camera.position.z - self.camera.target.z,
        )
        radius = offset.magnitude()
        if radius == 0.0:
            raise ValueError("camera position must differ from target for orbit operations")
        yaw = math.atan2(offset.x, offset.z) + math.radians(float(yaw_degrees))
        pitch = math.asin(max(-1.0, min(1.0, offset.y / radius))) + math.radians(float(pitch_degrees))
        pitch = max(math.radians(-89.0), min(math.radians(89.0), pitch))
        x = radius * math.sin(yaw) * math.cos(pitch)
        y = radius * math.sin(pitch)
        z = radius * math.cos(yaw) * math.cos(pitch)
        self.camera.position = Point3D(self.camera.target.x + x, self.camera.target.y + y, self.camera.target.z + z)
