"""Tests for Partitioned Consumer Group."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_partitioned_consumer_group import partitioned_consumer_group
except ImportError:
    from p01_partitioned_consumer_group import partitioned_consumer_group


def test_partitioned_consumer_group():
    alloc = partitioned_consumer_group([0, 1, 2, 3, 4], ['c1', 'c2'])
    assert alloc['c1'] == [0, 2, 4]
    assert alloc['c2'] == [1, 3]
    assert partitioned_consumer_group([0, 1], []) == {}
