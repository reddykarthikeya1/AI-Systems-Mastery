"""Problem 01 — Cross Encoder Rerank Sort

Topic: 05 Multi Stage Retrieval and Reranking
Target: Production-grade implementation

Re-rank candidate documents using cross-encoder relevance scores and threshold.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def cross_encoder_rerank_sort(candidates: list[tuple[str, float]], min_score_threshold: float = 0.5) -> list[tuple[str, float]]:
    """candidates: list of (doc_id, score).
    Filter candidates with score >= min_score_threshold.
    Sort by score descending.
    Returns filtered, sorted list.
    """
    raise NotImplementedError("Implement cross_encoder_rerank_sort")
