from typing import TypedDict
from gauze.collection import Collection


def test_build_collection_from_sequence():
    col = Collection((1, 2, 3))
    assert list(col) == [1, 2, 3]


def test_build_collection_from_generator():
    col = Collection(range(10))
    assert list(col) == list(range(10))


def test_typing():
    collection: Collection[int] = Collection((1, 2, 3))
    assert collection[0] == 1


def test_filtering_with_lambda():
    collection: Collection[int] = Collection(range(10))
    result = collection.where(lambda a: a == 1)
    assert list(result) == [1]


def test_filtering_with_expression():
    class Value(TypedDict):
        a: int
        b: int

    collection = Collection([Value(a=1, b=2), Value(a=3, b=4)])
    result = collection["a"]
    assert list(result)
