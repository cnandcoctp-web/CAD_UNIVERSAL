"""Reusable decorators for EvilTech CAD."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar

from UTILS.timers import Stopwatch

T = TypeVar("T")


def timed(func: Callable[..., T]) -> Callable[..., tuple[T, float]]:
    """Return the function result paired with elapsed runtime."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> tuple[T, float]:
        stopwatch = Stopwatch()
        result = func(*args, **kwargs)
        return result, stopwatch.elapsed()

    return wrapper


def retry(attempts: int = 3, exceptions: tuple[type[BaseException], ...] = (Exception,)) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Retry a function for a bounded number of attempts."""

    def decorate(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_error: BaseException | None = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_error = exc
            assert last_error is not None
            raise last_error

        return wrapper

    return decorate
