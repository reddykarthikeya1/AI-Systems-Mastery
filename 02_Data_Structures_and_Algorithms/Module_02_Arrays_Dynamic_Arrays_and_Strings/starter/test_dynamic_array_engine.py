"""Unit tests for DynamicArrayEngine."""
import pytest
from dynamic_array_engine import DynamicArrayEngine


def test_initialization():
    arr = DynamicArrayEngine[int](initial_capacity=4)
    assert len(arr) == 0
    assert arr.capacity == 4
    assert arr.reallocation_count == 0


def test_append_and_geometric_growth():
    arr = DynamicArrayEngine[int](initial_capacity=2)
    arr.append(10)
    arr.append(20)
    assert len(arr) == 2
    assert arr.capacity == 2
    assert arr.reallocation_count == 0

    # Triggers resize to 4
    arr.append(30)
    assert len(arr) == 3
    assert arr.capacity == 4
    assert arr.reallocation_count == 1
    assert arr[0] == 10
    assert arr[1] == 20
    assert arr[2] == 30


def test_negative_indexing_and_out_of_bounds():
    arr = DynamicArrayEngine[str]()
    arr.append("alpha")
    arr.append("beta")
    assert arr[-1] == "beta"
    assert arr[-2] == "alpha"

    with pytest.raises(IndexError):
        _ = arr[2]
    with pytest.raises(IndexError):
        _ = arr[-3]


def test_pop_and_compaction():
    arr = DynamicArrayEngine[int](initial_capacity=16)
    for i in range(16):
        arr.append(i)
    assert arr.capacity == 16

    # Pop down to 4 elements (<= 25% of 16), capacity should shrink to 8
    for _ in range(12):
        arr.pop()
    assert len(arr) == 4
    assert arr.capacity == 8


def test_in_place_reversal():
    arr = DynamicArrayEngine[int]()
    for x in [1, 2, 3, 4, 5]:
        arr.append(x)
    arr.reverse_in_place()
    assert arr.to_list() == [5, 4, 3, 2, 1]


def test_sliding_window_max_sum():
    arr = DynamicArrayEngine[int]()
    for x in [2, 1, 5, 1, 3, 2]:
        arr.append(x)
    assert arr.max_sliding_window_sum(3) == 9  # [5, 1, 3]


def test_prefix_sums():
    arr = DynamicArrayEngine[int]()
    for x in [1, 2, 3, 4]:
        arr.append(x)
    assert arr.prefix_sums() == [0, 1, 3, 6, 10]
def test_empty_array_edge_cases():
    arr = DynamicArrayEngine[int]()
    assert len(arr) == 0
    assert arr.to_list() == []
    with pytest.raises(IndexError):
        arr.pop()
    with pytest.raises(IndexError):
        _ = arr[0]


def test_single_element_and_reversal_edge_cases():
    arr = DynamicArrayEngine[int]()
    arr.append(42)
    assert len(arr) == 1
    assert arr[0] == 42
    assert arr[-1] == 42
    arr.reverse_in_place()
    assert arr.to_list() == [42]
    val = arr.pop()
    assert val == 42
    assert len(arr) == 0


def test_boundary_window_and_prefix_edge_cases():
    arr = DynamicArrayEngine[int]()
    arr.append(5)
    arr.append(10)
    arr.append(15)
    # Window equal to length
    assert arr.max_sliding_window_sum(3) == 30
    # Window size 1
    assert arr.max_sliding_window_sum(1) == 15
    # Oversized window raises ValueError
    with pytest.raises(ValueError):
        arr.max_sliding_window_sum(5)
    # Prefix sums on empty
    empty_arr = DynamicArrayEngine[int]()
    assert empty_arr.prefix_sums() == [0]
