from gauze.matchers import is_matcher


def test_is_matcher():
    assert is_matcher(lambda val: True)
