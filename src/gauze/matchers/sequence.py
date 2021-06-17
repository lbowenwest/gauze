from typing import Sequence, Sized, TypeVar, Union

from .base import Matcher
from .helpers import as_matcher

T = TypeVar("T")


class EmptyMatcher(Matcher[Sized]):
    def match(self, actual: Sized) -> bool:
        try:
            return len(actual) == 0
        except TypeError:
            return False


class ContainsMatcher(Matcher[Sequence[T]]):
    def __init__(self, element_matcher: Matcher[T]) -> None:
        self.matcher = element_matcher

    def match(self, actual: Sequence[T]) -> bool:
        try:
            for element in actual:
                if self.matcher.match(element):
                    return True
        except TypeError:
            pass
        return False


class ContainsOnlyMatcher(Matcher[Sequence[T]]):
    def __init__(self, element_matcher: Matcher[T]) -> None:
        self.matcher = element_matcher

    def match(self, actual: Sequence[T]) -> bool:
        try:
            sequence = list(actual)
            if len(sequence) == 0:
                return False
            for element in sequence:
                if not self.matcher.match(element):
                    return False
            return True
        except TypeError:
            return False


def empty() -> Matcher[Sized]:
    return EmptyMatcher()


def contains(match: Union[Matcher[T], T]) -> Matcher[Sequence[T]]:
    return ContainsMatcher(as_matcher(match))
