"""Tests for Softmax Stable Derivatives."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_softmax_stable_derivatives import softmax_stable_derivatives
except ImportError:
    from p01_softmax_stable_derivatives import softmax_stable_derivatives


def test_softmax_stable_derivatives():
    probs = softmax_stable_derivatives([1000.0, 1001.0, 1002.0])
    assert len(probs) == 3
    assert abs(sum(probs) - 1.0) < 1e-3
    assert probs[2] > probs[1] > probs[0]
