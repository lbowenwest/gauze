from hypothesis import given
from hypothesis import strategies as st

from gauze.matchers import (
    Matcher,
    anything,
    all_of,
    any_of,
    equal_to,
    not_,
    greater_than,
    greater_than_or_equal_to,
    less_than,
    less_than_or_equal_to,
    starts_with,
    contains,
)


def test_calling_matcher():
    class TestMatcher(Matcher):
        def __init__(self):
            self.value = False

        def match(self, actual) -> bool:
            self.value = True
            return self.value

    matcher = TestMatcher()
    assert not matcher.value
    matcher(1)
    assert matcher.value


@given(st.lists(st.integers()))
def test_anything_matcher(input_list):
    filtered_list = list(filter(anything, input_list))
    assert len(input_list) == len(filtered_list)


@given(st.lists(st.integers()))
def test_equal_to_matcher(input_list):
    filtered_list = filter(equal_to(4), input_list)
    assert all(a == 4 for a in filtered_list)


@given(st.lists(st.integers()))
def test_not_matcher(input_list):
    filtered_list = filter(not_(equal_to(1)), input_list)
    assert not any(a == 1 for a in filtered_list)


@given(st.lists(st.integers()))
def test_greater_than_matcher(input_list):
    filtered_list = filter(greater_than(4), input_list)
    assert all(a > 4 for a in filtered_list)


@given(st.lists(st.integers()))
def test_greater_than_or_equal_to_matcher(input_list):
    filtered_list = filter(greater_than_or_equal_to(4), input_list)
    assert all(a >= 4 for a in filtered_list)


@given(st.lists(st.integers()))
def test_less_than_matcher(input_list):
    filtered_list = filter(less_than(0), input_list)
    assert all(a < 0 for a in filtered_list)


@given(st.lists(st.integers()))
def test_less_than_or_equal_to_matcher(input_list):
    filtered_list = filter(less_than_or_equal_to(0), input_list)
    assert all(a <= 0 for a in filtered_list)


@given(st.lists(st.integers()))
def test_any_of_matcher(input_list):
    filtered_list = filter(any_of(equal_to(0), equal_to(1)), input_list)
    assert all(a == 0 or a == 1 for a in filtered_list)


@given(st.lists(st.integers()))
def test_all_of_matcher(input_list):
    filtered_list = filter(all_of(greater_than(0), less_than(10)), input_list)
    assert all(0 < a < 10 for a in filtered_list)


@given(st.lists(st.text()))
def test_starts_with_matcher(input_list):
    filtered_list = filter(starts_with("a"), input_list)
    assert all(a.startswith("a") for a in filtered_list)


@given(st.lists(st.lists(st.characters(), max_size=10)))
def test_contains_matcher(input_list):
    filtered_list = filter(contains("a"), input_list)
    assert all("a" in a for a in filtered_list)


@given(st.lists(st.one_of(st.lists(st.integers()), st.none())))
def test_contains_matcher_handles_none(input_list):
    filtered_list = filter(contains(0), input_list)
    assert all(0 in a for a in filtered_list)


@given(st.lists(st.one_of(st.integers(), st.text())))
def test_composite_matchers(input_list):
    matcher = any_of(all_of(greater_than(0), less_than(10)), starts_with("a"))
    filtered_list = filter(matcher, input_list)
    for element in filtered_list:
        if isinstance(element, str):
            assert element.startswith("a")
        elif isinstance(element, int):
            assert 0 < element < 10
        else:
            assert False, "unexpected item in list"
