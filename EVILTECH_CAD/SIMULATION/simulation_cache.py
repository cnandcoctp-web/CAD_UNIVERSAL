"""Result cache for simulation framework artifacts."""

from __future__ import annotations

from UTILS.cache import TTLCache


class SimulationCache(TTLCache[object]):
    """Cache simulation outputs by derived cache key."""

    pass