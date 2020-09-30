from typing import Mapping, TypeVar, Union, overload

from .base import Matcher
from .core import all_of, anything
from .helpers import as_matcher

V = TypeVar("V")


class PropertyMatcher(Matcher[object]):
    def __init__(self, property_name: str, value_matcher: Matcher[V]) -> None:
        self.property_name = property_name
        self.value_matcher = value_matcher

    def match(self, actual: object) -> bool:
        if actual is None or not hasattr(actual, self.property_name):
            return False

        value = getattr(actual, self.property_name)
        return self.value_matcher.match(value)


def has_property(
    name: str,
    match: Union[None, Matcher[V], V] = None,
) -> Matcher[object]:
    if match is None:
        match = anything()
    return PropertyMatcher(name, as_matcher(match))


@overload
def has_properties(**value_matchers: Union[Matcher[V], V]) -> Matcher[object]:
    ...


@overload
def has_properties(kv_matchers: Mapping[str, Union[Matcher[V], V]]) -> Matcher[object]:
    ...


def has_properties(kv_matchers=None, /, **value_matchers):
    mapper = kv_matchers or {}
    mapper.update(value_matchers)
    return all_of(*[has_property(name, matcher) for name, matcher in mapper.items()])
