"""Import management for EvilTech CAD project data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from IO.file_manager import FileFormatRegistry


class ImportManager:
    """Import serialized data through the registered file-format registry."""

    def __init__(self, registry: FileFormatRegistry) -> None:
        if not isinstance(registry, FileFormatRegistry):
            raise TypeError("registry must be a FileFormatRegistry")
        self.registry = registry

    def import_data(self, path: Path, format_name: str) -> Any:
        """Import data from a file using a registered format."""
        extension = self.registry.resolve_extension(format_name)
        file_path = Path(path)
        if file_path.suffix != extension:
            raise ValueError(f"File extension '{file_path.suffix}' does not match format '{format_name}'")
        if format_name != "json":
            raise ValueError(f"Unsupported import format '{format_name}'")
        with file_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
