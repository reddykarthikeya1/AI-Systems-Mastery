"""Tests for Jaccard Similarity Sets."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_jaccard_similarity_sets import jaccard_similarity_sets
except ImportError:
    from p01_jaccard_similarity_sets import jaccard_similarity_sets


def test_jaccard_similarity_sets():
    sim, dist = jaccard_similarity_sets({'a', 'b', 'c'}, {'b', 'c', 'd'})
    assert sim == 0.5 and dist == 0.5
    assert jaccard_similarity_sets(set(), set()) == (1.0, 0.0)
