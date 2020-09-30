import operator
from typing import Any, Callable

from .base import Matcher


class ComparisonMatcher(Matcher[Any]):
    def __init__(self, value: Any, operator_func: Callable[[Any, Any], bool]):
        self.value = value
        self.operator = operator_func

    def match(self, actual: Any) -> bool:
        try:
            return self.operator(actual, self.value)
        except TypeError:
            return False


def greater_than(value: Any) -> Matcher[Any]:
    return ComparisonMatcher(value, operator.gt)


def greater_than_or_equal_to(value: Any) -> Matcher[Any]:
    return ComparisonMatcher(value, operator.ge)


def less_than(value: Any) -> Matcher[Any]:
    return ComparisonMatcher(value, operator.lt)


def less_than_or_equal_to(value: Any) -> Matcher[Any]:
    return ComparisonMatcher(value, operator.le)
