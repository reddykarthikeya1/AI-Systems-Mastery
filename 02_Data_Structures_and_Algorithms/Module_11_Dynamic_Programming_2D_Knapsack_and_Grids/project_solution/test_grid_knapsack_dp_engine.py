"""Unit tests for GridKnapsackDPEngine."""
from grid_knapsack_dp_engine import GridKnapsackDPEngine


def test_knapsack_01_with_reconstruction():
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 8]
    capacity = 5
    max_val, items = GridKnapsackDPEngine.knapsack_01(weights, values, capacity)
    # Optimum: item 0 (w=2, v=3) and item 1 (w=3, v=4) -> val=7, OR item 3 (w=5, v=8) -> val=8
    assert max_val == 8
    assert items == [3]

def test_longest_common_subsequence():
    assert GridKnapsackDPEngine.longest_common_subsequence("abcde", "ace") == 3
    assert GridKnapsackDPEngine.longest_common_subsequence("abc", "abc") == 3
    assert GridKnapsackDPEngine.longest_common_subsequence("abc", "def") == 0

def test_edit_distance():
    assert GridKnapsackDPEngine.edit_distance("horse", "ros") == 3
    assert GridKnapsackDPEngine.edit_distance("intention", "execution") == 5

def test_knapsack_zero_capacity():
    val, items = GridKnapsackDPEngine.knapsack_01([1, 2], [10, 20], 0)
    assert val == 0
    assert items == []

def test_knapsack_empty_items():
    val, items = GridKnapsackDPEngine.knapsack_01([], [], 10)
    assert val == 0
    assert items == []

def test_edit_distance_empty_strings():
    assert GridKnapsackDPEngine.edit_distance("", "") == 0
    assert GridKnapsackDPEngine.edit_distance("abc", "") == 3
    assert GridKnapsackDPEngine.edit_distance("", "xyz") == 3
