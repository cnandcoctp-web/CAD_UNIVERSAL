"""Plugin discovery framework for the EvilTech CAD foundation layer.

The initial implementation provides a safe, empty discovery mechanism that can
be extended later with manifest-based plugin loading. The public interface is
intentionally simple and deterministic.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Sequence


class PluginDiscoveryFramework:
    """Discover plugin manifests from configured search roots."""

    def discover_plugins(self, search_roots: Sequence[Path] | None = None) -> List[Path]:
        """Search for plugin manifests in the provided directories.

        Args:
            search_roots: Directories to scan for plugin manifests.

        Returns:
            A list of discovered manifest paths.
        """
        if search_roots is None:
            return []

        manifests: List[Path] = []
        for root in search_roots:
            if not root.exists():
                continue
            for candidate in sorted(root.rglob("plugin.json")):
                if candidate.is_file():
                    manifests.append(candidate)
        return manifests
