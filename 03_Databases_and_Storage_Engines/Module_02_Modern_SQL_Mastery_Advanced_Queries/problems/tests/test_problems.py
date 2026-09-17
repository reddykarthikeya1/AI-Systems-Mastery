"""Tests for Evaluate Window Frame."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_evaluate_window_frame import evaluate_window_frame
except ImportError:
    from p01_evaluate_window_frame import evaluate_window_frame


def test_evaluate_window_frame():
    assert evaluate_window_frame([10.0, 20.0, 30.0, 40.0]) == [10.0, 30.0, 50.0, 70.0]
    assert evaluate_window_frame([]) == []
    assert evaluate_window_frame([5.0]) == [5.0]
