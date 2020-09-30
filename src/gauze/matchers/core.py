from typing import Any, TypeVar, Union

from .base import Matcher
from .helpers import as_matcher

T = TypeVar("T")


class AnythingMatcher(Matcher[Any]):
    def match(self, actual: Any) -> bool:
        return True


class NotMatcher(Matcher[T]):
    def __init__(self, matcher: Matcher[T]) -> None:
        self.matcher = matcher

    def match(self, actual: T) -> bool:
        return not self.matcher(actual)


class AnyOfMatcher(Matcher[T]):
    def __init__(self, *matchers: Matcher[T]) -> None:
        self.matchers = matchers

    def match(self, actual: T) -> bool:
        return any(matcher(actual) for matcher in self.matchers)


class AllOfMatcher(Matcher[T]):
    def __init__(self, *matchers: Matcher[T]) -> None:
        self.matchers = matchers

    def match(self, actual: T) -> bool:
        return all(matcher(actual) for matcher in self.matchers)


def anything() -> Matcher[Any]:
    return AnythingMatcher()


def not_(match: Union[Matcher[T], T]) -> Matcher[T]:
    return NotMatcher(as_matcher(match))


def all_of(*items: Union[Matcher[T], T]) -> Matcher[T]:
    return AllOfMatcher(*[as_matcher(item) for item in items])


def any_of(*items: Union[Matcher[T], T]) -> Matcher[T]:
    return AnyOfMatcher(*[as_matcher(item) for item in items])
