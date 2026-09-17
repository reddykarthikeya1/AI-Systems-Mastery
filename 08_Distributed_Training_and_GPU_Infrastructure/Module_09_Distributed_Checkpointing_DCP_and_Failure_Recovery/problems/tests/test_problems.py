"""Tests for Sharded State Dict Merge."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_sharded_state_dict_merge import sharded_state_dict_merge
except ImportError:
    from p01_sharded_state_dict_merge import sharded_state_dict_merge


def test_sharded_state_dict_merge():
    shards = [(1, [3.0, 4.0]), (0, [1.0, 2.0])]
    assert sharded_state_dict_merge(shards) == [1.0, 2.0, 3.0, 4.0]
