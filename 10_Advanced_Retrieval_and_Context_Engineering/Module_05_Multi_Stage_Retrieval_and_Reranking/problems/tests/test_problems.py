"""Tests for Cross Encoder Rerank Sort."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_cross_encoder_rerank_sort import cross_encoder_rerank_sort
except ImportError:
    from p01_cross_encoder_rerank_sort import cross_encoder_rerank_sort


def test_cross_encoder_rerank_sort():
    cands = [("d1", 0.3), ("d2", 0.9), ("d3", 0.6)]
    reranked = cross_encoder_rerank_sort(cands, 0.5)
    assert reranked == [("d2", 0.9), ("d3", 0.6)]
