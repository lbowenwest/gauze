from typing import TypeVar, Union

from .base import Matcher
from .equal import equal_to

T = TypeVar("T")


def as_matcher(value: Union[Matcher[T], T]) -> Matcher[T]:
    if isinstance(value, Matcher):
        return value
    else:
        return equal_to(value)
