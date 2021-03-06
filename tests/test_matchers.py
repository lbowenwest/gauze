import pytest
from hypothesis import given
from hypothesis import strategies as st

from gauze.matchers import (
    all_of,
    any_of,
    anything,
    contains,
    ends_with,
    equal_to,
    greater_than,
    greater_than_or_equal_to,
    less_than,
    less_than_or_equal_to,
    not_,
    starts_with,
)


@given(st.lists(st.integers()))
def test_anything_matcher(input_list):
    filtered_list = list(filter(anything(), input_list))
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


def test_starts_with_raises_when_strict():
    with pytest.raises(AttributeError):
        starts_with("a", strict=True).match(1)  # type: ignore
    assert not starts_with("a", strict=False).match(1)  # type: ignore


@given(st.lists(st.text()))
def test_ends_with_matcher(input_list):
    filtered_list = filter(ends_with("a"), input_list)
    assert all(a.endswith("a") for a in filtered_list)


def test_ends_with_raises_when_strict():
    with pytest.raises(AttributeError):
        ends_with("a", strict=True).match(1)  # type: ignore
    assert not ends_with("a", strict=False).match(1)  # type: ignore


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
            raise AssertionError("unexpected item in list")
