"""Tests for Online Softmax Rescaling."""
from __future__ import annotations

import pytest
from p01_online_softmax_rescaling import online_softmax_rescaling


def test_online_softmax_rescaling():
    # Two identical blocks: max 10.0, sum 5.0
    m, s = online_softmax_rescaling(10.0, 5.0, 10.0, 5.0)
    assert m == 10.0 and s == 10.0
    # Block 2 has higher max
    m2, s2 = online_softmax_rescaling(5.0, 2.0, 10.0, 3.0)
    assert m2 == 10.0
