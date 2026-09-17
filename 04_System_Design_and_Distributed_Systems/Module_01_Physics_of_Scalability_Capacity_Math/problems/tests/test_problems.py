"""Tests for Little Law Concurrency."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_little_law_concurrency import little_law_concurrency
except ImportError:
    from p01_little_law_concurrency import little_law_concurrency


def test_little_law_concurrency():
    assert little_law_concurrency(5000.0, 0.05) == 250.0
    assert little_law_concurrency(0.0, 1.0) == 0.0
