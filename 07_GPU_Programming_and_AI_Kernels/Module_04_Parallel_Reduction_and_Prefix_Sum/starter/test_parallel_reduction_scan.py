"""Unit tests for Parallel Reduction and Scan Engine."""
from __future__ import annotations

import numpy as np
import pytest
from parallel_reduction_scan import (
    blelloch_scan_exclusive,
    blelloch_scan_inclusive,
    block_tree_reduce,
    warp_shuffle_down_reduce,
)


def test_warp_shuffle_down_reduce() -> None:
    vals = [float(i + 1) for i in range(32)]
    # Sum of 1 to 32 is 32 * 33 / 2 = 528
    result = warp_shuffle_down_reduce(vals)
    assert pytest.approx(result, rel=1e-5) == 528.0


def test_block_tree_reduce() -> None:
    arr = np.linspace(1.0, 1000.0, 1000, dtype=np.float64)
    expected_sum = float(np.sum(arr))
    actual_sum = block_tree_reduce(arr, block_size=128)
    assert pytest.approx(actual_sum, rel=1e-5) == expected_sum


def test_blelloch_prefix_scan() -> None:
    arr = np.array([3, 1, 7, 0, 4, 1, 6, 3], dtype=np.float64)

    # Inclusive scan matches np.cumsum
    inclusive = blelloch_scan_inclusive(arr)
    expected_inc = np.cumsum(arr)
    np.testing.assert_allclose(inclusive, expected_inc)

    # Exclusive scan: [0, 3, 4, 11, 11, 15, 16, 22]
    exclusive = blelloch_scan_exclusive(arr)
    expected_exc = np.array([0, 3, 4, 11, 11, 15, 16, 22], dtype=np.float64)
    np.testing.assert_allclose(exclusive, expected_exc)
