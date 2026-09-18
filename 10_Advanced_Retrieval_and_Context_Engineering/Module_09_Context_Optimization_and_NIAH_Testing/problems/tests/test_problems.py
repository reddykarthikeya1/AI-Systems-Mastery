"""Tests for Needle In Haystack Evaluator."""
from __future__ import annotations

import pytest
from p01_needle_in_haystack_evaluator import needle_in_haystack_evaluator


def test_needle_in_haystack_evaluator():
    contexts = [
        (10.0, "secret key is 42"),
        (50.0, "nothing here"),
        (90.0, "secret key is 42")
    ]
    res = needle_in_haystack_evaluator("42", contexts)
    assert res['overall_accuracy_pct'] == 66.67
    assert res['min_depth_failure'] == 50.0
