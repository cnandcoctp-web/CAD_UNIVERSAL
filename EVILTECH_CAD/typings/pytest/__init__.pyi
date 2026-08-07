from typing import Any, ContextManager, Generic, TypeVar

_T = TypeVar("_T")

class ApproxBase: ...

def approx(expected: Any, rel: float | None = ..., abs: float | None = ..., nan_ok: bool = ...) -> Any: ...

class RaisesContext(ContextManager[Exception], Generic[_T]):
    value: _T

def raises(expected_exception: type[_T], *args: Any, **kwargs: Any) -> RaisesContext[_T]: ...
