from .base import Matcher


class ContainsMatcher(Matcher):
    def __init__(self, value):
        self.value = value

    def __call__(self, actual) -> bool:
        try:
            return self.value in actual
        except TypeError:
            return False


def contains(value) -> ContainsMatcher:
    return ContainsMatcher(value)
