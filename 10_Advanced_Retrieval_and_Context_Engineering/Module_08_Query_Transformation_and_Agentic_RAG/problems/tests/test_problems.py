"""Pytest suite for Query Transformation and Agentic RAG problem bank."""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

# Test the solution by default, or stub if imported from problems/
SOL_DIR = Path(__file__).resolve().parent.parent / "solutions"
PROB_DIR = Path(__file__).resolve().parent.parent
if Path.cwd().resolve() == PROB_DIR.resolve():
    if str(PROB_DIR) not in sys.path:
        sys.path.insert(0, str(PROB_DIR))
else:
    if str(SOL_DIR) not in sys.path:
        sys.path.insert(0, str(SOL_DIR))

from p01_compute_rrf_scores import compute_rrf_scores


def test_compute_rrf_scores():
    r1 = ["doc_a", "doc_b", "doc_c"]
    r2 = ["doc_b", "doc_a", "doc_d"]
    merged = compute_rrf_scores([r1, r2], k=60)
    # doc_a: 1/61 + 1/62 = 0.016393 + 0.016129 = 0.032522
    # doc_b: 1/62 + 1/61 = 0.032522
    assert "doc_a" in merged and "doc_b" in merged
    assert merged["doc_a"] == merged["doc_b"]
    assert merged["doc_a"] > merged["doc_c"]

