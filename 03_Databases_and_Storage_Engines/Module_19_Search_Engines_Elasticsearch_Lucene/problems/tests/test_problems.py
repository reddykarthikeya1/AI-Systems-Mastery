"""Tests for Bm25 Score Tokens."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_bm25_score_tokens import bm25_score_tokens
except ImportError:
    from p01_bm25_score_tokens import bm25_score_tokens


def test_bm25_score_tokens():
    score = bm25_score_tokens(
        query_terms=["database", "acid"],
        doc_tokens=["database", "storage", "database", "acid", "engine"],
        avg_doc_len=5.0,
        doc_freqs={"database": 10, "acid": 5},
        total_docs=100
    )
    assert score > 0.0
    assert bm25_score_tokens(["unknown"], ["a", "b"], 2.0, {}, 10) == 0.0
