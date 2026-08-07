"""Export management for EvilTech CAD project data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from IO.file_manager import FileFormatRegistry


class ExportManager:
    """Export serialized data through the registered file-format registry."""

    def __init__(self, registry: FileFormatRegistry) -> None:
        if not isinstance(registry, FileFormatRegistry):
            raise TypeError("registry must be a FileFormatRegistry")
        self.registry = registry

    def export_data(self, payload: Any, path: Path, format_name: str) -> Path:
        """Export data to disk using a registered format."""
        extension = self.registry.resolve_extension(format_name)
        file_path = Path(path)
        if file_path.suffix != extension:
            raise ValueError(f"File extension '{file_path.suffix}' does not match format '{format_name}'")
        if format_name != "json":
            raise ValueError(f"Unsupported export format '{format_name}'")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
        return file_path
