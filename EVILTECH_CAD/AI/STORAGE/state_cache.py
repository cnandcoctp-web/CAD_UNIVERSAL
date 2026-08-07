"""State cache for AI processing artifacts."""

from __future__ import annotations

from UTILS.cache import TTLCache


class AIStateCache(TTLCache[object]):
    """Typed alias for cached AI artifacts."""

    pass
