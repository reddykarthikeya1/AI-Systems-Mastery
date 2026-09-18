"""Tests for Exact Match F1 Score."""
from __future__ import annotations

import pytest
from p01_exact_match_f1_score import exact_match_f1_score


def test_exact_match_f1_score():
    em, f1 = exact_match_f1_score("The Eiffel Tower", "eiffel tower")
    assert em == 0
    assert f1 > 0.7
    em2, f1_2 = exact_match_f1_score("Paris", "Paris")
    assert em2 == 1 and f1_2 == 1.0
