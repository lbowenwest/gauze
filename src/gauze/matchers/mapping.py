from typing import Hashable, Mapping, TypeVar, Union, overload

from .base import Matcher
from .helpers import as_matcher

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class HasEntriesMatcher(Matcher[Mapping[K, V]]):
    def __init__(self, value_matchers: Mapping[K, Matcher[V]]):
        self.value_matchers = sorted(value_matchers.items())

    def match(self, actual: Mapping[K, V]) -> bool:
        # for key, value_matcher in self.value_matchers:
        #     pass
        return True


@overload
def has_entries(kv_matcher: Mapping[K, Union[Matcher[V], V]]) -> Matcher[Mapping[K, V]]:
    ...


@overload
def has_entries(**v_matchers: Union[Matcher[V], V]) -> Matcher[Mapping[str, V]]:
    ...


def has_entries(kv_matcher=None, /, **v_matchers):
    mapper = kv_matcher or {}
    mapper.update(v_matchers)
    return HasEntriesMatcher({k: as_matcher(v) for k, v in mapper.items()})
