"""Tests for Skip List Probabilistic Index."""
from __future__ import annotations

import pytest
from p01_skip_list_probabilistic_index import skip_list_probabilistic_index


def test_skip_list_probabilistic_index():
    l2 = {10: 50}
    l1 = {10: 30, 30: 50}
    l0 = {10: 20, 20: 30, 30: 40, 40: 50}
    assert skip_list_probabilistic_index([l2, l1, l0], 30) == 30
    assert skip_list_probabilistic_index([l2, l1, l0], 25) is None
