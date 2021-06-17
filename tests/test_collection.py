from gauze.collection import Collection


def test_build_collection_from_sequence():
    col = Collection(1, 2, 3)
    assert list(col) == [1, 2, 3]


def test_build_collection_from_generator():
    col = Collection(range(10))
    assert list(col) == list(range(10))


def test_typing():
    collection: Collection[int] = Collection(1, 2, 3)
    assert collection[0] == 1
