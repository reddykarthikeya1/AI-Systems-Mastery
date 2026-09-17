"""Tests for Bootstrap Confidence Interval."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_bootstrap_confidence_interval import bootstrap_confidence_interval
except ImportError:
    from p01_bootstrap_confidence_interval import bootstrap_confidence_interval


def test_bootstrap_confidence_interval():
    estimates = list(range(100))  # 0 to 99
    low, high = bootstrap_confidence_interval(estimates, alpha=0.1)
    assert low == 5.0
    assert high == 94.0
