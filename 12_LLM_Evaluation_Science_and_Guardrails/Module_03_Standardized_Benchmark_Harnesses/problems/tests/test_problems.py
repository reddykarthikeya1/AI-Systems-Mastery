"""Tests for Multiple Choice Evaluator."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_multiple_choice_evaluator import multiple_choice_evaluator
except ImportError:
    from p01_multiple_choice_evaluator import multiple_choice_evaluator


def test_multiple_choice_evaluator():
    preds = ["A", "b ", "C", "d"]
    gts = ["A", "B", "C", "A"]
    acc = multiple_choice_evaluator(preds, gts)
    assert acc == 75.0
