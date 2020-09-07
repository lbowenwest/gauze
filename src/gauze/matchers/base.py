from typing import Any

from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class Matcher(Protocol):
    """
    Matcher is anything that is callable with one argument and returns a bool
    """

    def __call__(self, actual: Any) -> bool:
        ...


def is_matcher(value: Any) -> bool:
    return isinstance(value, Matcher)
