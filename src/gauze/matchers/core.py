from typing import Any

from .base import Matcher


class EqualMatcher(Matcher):
    def __init__(self, value):
        self.value = value

    def __call__(self, actual: Any) -> bool:
        return actual == self.value


class AnythingMatcher(Matcher):
    def __call__(self, actual: Any) -> bool:
        return True


class AnyOfMatcher(Matcher):
    def __init__(self, *matchers: Matcher) -> None:
        self.matchers = matchers

    def __call__(self, actual: Any) -> bool:
        return any(matcher(actual) for matcher in self.matchers)


class AllOfMatcher(Matcher):
    def __init__(self, *matchers: Matcher) -> None:
        self.matchers = matchers

    def __call__(self, actual: Any) -> bool:
        return all(matcher(actual) for matcher in self.matchers)


class NotMatcher(Matcher):
    def __init__(self, matcher: Matcher) -> None:
        self.matcher = matcher

    def __call__(self, actual: Any) -> bool:
        return not self.matcher(actual)


anything = AnythingMatcher()


def equal_to(value: Any) -> EqualMatcher:
    return EqualMatcher(value)


def any_of(*matchers: Matcher) -> AnyOfMatcher:
    return AnyOfMatcher(*matchers)


def all_of(*matchers: Matcher) -> AllOfMatcher:
    return AllOfMatcher(*matchers)


def not_(matcher: Matcher) -> NotMatcher:
    return NotMatcher(matcher)
