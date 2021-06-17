from __future__ import annotations

from functools import partial
from operator import attrgetter
from typing import (
    Any,
    Generator,
    Generic,
    Iterator,
    List,
    Type,
    TypeVar,
    Union,
    overload,
    Iterable,
    Tuple,
    Optional,
    Sequence,
    Callable,
)

from pydantic import ValidationError
from pydantic.fields import ModelField

from .matchers.base import Matcher
from .matchers.object import has_properties

T = TypeVar("T")


def get_value(instance: object, name: str) -> Any:
    """
    Function that gets an attribute for an object

    Has various fallback options to get the value
    """
    if hasattr(instance, name):
        return getattr(instance, name)
    elif hasattr(instance, "get") and callable(instance.get):
        return instance.get(name)

    return None


class DataObject(object):
    def __init__(self, **kwargs) -> None:
        if kwargs:
            self.__dict__.update(kwargs)

    def __repr__(self):
        return (
            "{" + ", ".join(f"{k}: {v}" for k, v in sorted(self.__dict__.items())) + "}"
        )

    def __setattr__(self, key: str, value: Any) -> None:
        if key not in self.__dict__:
            super().__setattr__(key, value)
        else:
            raise AttributeError("can't set updating attributes")

    def __hasattr__(self, key: str):
        return key in self.__dict__

    def __getitem__(self, key: str) -> Any:
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"object has no attribute {key}")

    def __iter__(self):
        return self.__dict__.items()

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__

    def __eq__(self, other: object) -> bool:
        return self.__dict__ == other.__dict__

    def __ne__(self, other: object) -> bool:
        return not self == other

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()


class Collection(Generic[T]):
    def __init__(self, seq: Iterable[T] = ()) -> None:
        """
        Create a new collection from a sequence

        :param seq:
        """
        self.objects: List[T] = []
        self.objects.extend(seq)

    def __repr__(self):
        return f"<Collection: {repr(self.objects)}>"

    def __iter__(self) -> Iterator[T]:
        return iter(self.objects)

    def __len__(self) -> int:
        return len(self.objects)

    def __contains__(self, item: object) -> bool:
        return item in self.objects

    def __bool__(self) -> bool:
        return bool(self.objects)

    @classmethod
    def __validate__(
        cls: Type[Collection[T]], v: Any, field: ModelField
    ) -> Collection[T]:
        v = v if isinstance(v, cls) else cls(v)

        if not field.sub_fields:
            return v

        sub_field = field.sub_fields[0]
        errors = []
        for i, value in enumerate(v):
            _, error = sub_field.validate(value, {}, loc=(i,))
            if error:
                errors.append(error)

        if errors:
            raise ValidationError(errors, cls)
        return v

    @classmethod
    def __get_validators__(cls: Type[Collection[T]]) -> Generator[Any, None, None]:
        yield cls.__validate__

    @overload
    def __getitem__(self, item: int) -> T:
        ...

    @overload
    def __getitem__(self, item: slice) -> Collection[T]:
        ...

    @overload
    def __getitem__(self, *keys: str) -> Collection[Any]:
        ...

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.objects[item]
        elif isinstance(item, slice):
            return Collection(self.objects[item])
        elif isinstance(item, str):
            return Collection(map(partial(get_value, name=item), self.objects))
        else:
            return Collection(
                DataObject(**kv)
                for kv in map(
                    lambda d: dict(zip(item, attrgetter(*item)(d))),
                    self.objects,
                )
            )

    def __delitem__(self, item: Union[int, slice]) -> None:
        if isinstance(item, int):
            self.pop(item)
        elif isinstance(item, slice):
            objects_len = len(self.objects)
            for idx in sorted(range(*item.indices(objects_len)), reverse=True):
                self.pop(idx)
        else:
            raise TypeError("index must be int or slice")

    def pop(self, idx: int) -> T:
        return self.objects.pop(idx)

    @overload
    def where(self, matcher: Union[Matcher, Callable]) -> Collection[T]:
        ...

    @overload
    def where(self, **kwargs: Union[Matcher[Any], Any]) -> Collection[T]:
        ...

    def where(self, matcher=None, /, **kwargs):
        if matcher is None:
            matcher = has_properties(kwargs)
        return Collection(filter(matcher, self.objects))

    def copy(self) -> Collection[T]:
        return Collection(list(self.objects))

    def sort(self, *keys, reverse=False):
        raise NotImplementedError("not implemented")
