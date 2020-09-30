import re
from typing import Optional, Pattern, Union

from .base import Matcher


class StartsWithMatcher(Matcher[str]):
    def __init__(
        self,
        prefix: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
        strict: bool = False,
    ) -> None:
        self.prefix = prefix
        self.start = start
        self.end = end
        self.strict = strict

    def match(self, actual: str) -> bool:
        try:
            return actual.startswith(self.prefix, self.start, self.end)
        except AttributeError:
            if self.strict:
                raise
            return False


class EndsWithMatcher(Matcher[str]):
    def __init__(
        self,
        suffix: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
        strict: bool = False,
    ) -> None:
        self.suffix = suffix
        self.start = start
        self.end = end
        self.strict = strict

    def match(self, actual: str) -> bool:
        try:
            return actual.endswith(self.suffix, self.start, self.end)
        except AttributeError:
            if self.strict:
                raise
            return False


class RegexMatcher(Matcher[str]):
    def __init__(self, pattern: Pattern) -> None:
        self.pattern = pattern

    def match(self, actual: str) -> bool:
        return self.pattern.search(actual) is not None


def starts_with(
    prefix: str,
    start: Optional[int] = None,
    end: Optional[int] = None,
    *,
    strict: bool = False,
) -> Matcher[str]:
    return StartsWithMatcher(prefix, start, end, strict)


def ends_with(
    suffix: str,
    start: Optional[int] = None,
    end: Optional[int] = None,
    *,
    strict: bool = False,
) -> Matcher[str]:
    return EndsWithMatcher(suffix, start, end, strict)


def matches(pattern: Union[str, Pattern[str]]) -> Matcher[str]:
    if isinstance(pattern, str):
        pattern = re.compile(pattern)
    return RegexMatcher(pattern)
