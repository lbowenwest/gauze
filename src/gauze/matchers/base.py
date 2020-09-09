from typing import Any, Callable, Union

from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class Matcher(Protocol):
    def match(self, actual: Any) -> bool:
        ...  # pragma: no cover

    def __call__(self, actual: Any) -> bool:
        return self.match(actual)


MatcherFunc = Callable[[Any], bool]
Matchable = Union[Matcher, MatcherFunc]
