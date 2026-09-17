"""Tests for Cosine Similarity Matrix."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_cosine_similarity_matrix import cosine_similarity_matrix
except ImportError:
    from p01_cosine_similarity_matrix import cosine_similarity_matrix


def test_cosine_similarity_matrix():
    assert cosine_similarity_matrix([1.0, 0.0], [1.0, 0.0]) == 1.0
    assert cosine_similarity_matrix([1.0, 0.0], [0.0, 1.0]) == 0.0
    assert cosine_similarity_matrix([1.0, 1.0], [2.0, 2.0]) == 1.0
