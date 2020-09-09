import operator
from typing import Any

from .base import Matcher


class ComparisonMatcher(Matcher):
    def __init__(self, operator_func, value):
        self.operator = operator_func
        self.value = value

    def match(self, actual: Any) -> bool:
        try:
            return self.operator(actual, self.value)
        except TypeError:
            return False


def greater_than(value: Any) -> ComparisonMatcher:
    return ComparisonMatcher(operator.gt, value)


def greater_than_or_equal_to(value: Any) -> ComparisonMatcher:
    return ComparisonMatcher(operator.ge, value)


def less_than(value: Any) -> ComparisonMatcher:
    return ComparisonMatcher(operator.lt, value)


def less_than_or_equal_to(value: Any) -> ComparisonMatcher:
    return ComparisonMatcher(operator.le, value)


def starts_with(value: str) -> ComparisonMatcher:
    return ComparisonMatcher(str.startswith, value)
