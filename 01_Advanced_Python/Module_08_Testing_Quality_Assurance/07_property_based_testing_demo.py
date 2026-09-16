"""Module 08: Property-Based Testing with Hypothesis Demonstration.

Run with: pytest 03_property_based_testing_demo.py -v
"""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st


def custom_sort(numbers: list[int]) -> list[int]:
    """Sorts a list of numbers using Python's built-in Timsort."""
    return sorted(numbers)


# 1. Invariant 1: Length preservation
@given(st.lists(st.integers()))
def test_sort_preserves_length(numbers: list[int]) -> None:
    sorted_nums = custom_sort(numbers)
    assert len(sorted_nums) == len(numbers)


# 2. Invariant 2: Monotonic ordering
@given(st.lists(st.integers()))
def test_sort_is_monotonic(numbers: list[int]) -> None:
    sorted_nums = custom_sort(numbers)
    for i in range(len(sorted_nums) - 1):
        assert sorted_nums[i] <= sorted_nums[i + 1]


# 3. Invariant 3: Idempotence (sorting twice does not alter result)
@given(st.lists(st.integers()))
def test_sort_is_idempotent(numbers: list[int]) -> None:
    first_pass = custom_sort(numbers)
    second_pass = custom_sort(first_pass)
    assert first_pass == second_pass
