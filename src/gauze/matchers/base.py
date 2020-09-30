from typing import Generic, TypeVar

T = TypeVar("T")


class Matcher(Generic[T]):
    def match(self, actual: T) -> bool:
        ...  # pragma: no cover

    def __call__(self, actual: T) -> bool:
        return self.match(actual)
