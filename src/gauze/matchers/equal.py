from typing import Any

from .base import Matcher


class EqualMatcher(Matcher):
    def __init__(self, value):
        self.value = value

    def match(self, actual: Any) -> bool:
        return actual == self.value


def equal_to(value: Any) -> Matcher[Any]:
    return EqualMatcher(value)
