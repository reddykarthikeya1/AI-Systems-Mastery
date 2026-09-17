"""Tests for Bleu Ngram Overlap."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_bleu_ngram_overlap import bleu_ngram_overlap
except ImportError:
    from p01_bleu_ngram_overlap import bleu_ngram_overlap


def test_bleu_ngram_overlap():
    cand = ["the", "cat", "the", "cat"]
    ref = ["the", "cat", "on", "the", "mat"]
    assert bleu_ngram_overlap(cand, ref) == 0.75
    assert bleu_ngram_overlap(["dog"], ref) == 0.0
