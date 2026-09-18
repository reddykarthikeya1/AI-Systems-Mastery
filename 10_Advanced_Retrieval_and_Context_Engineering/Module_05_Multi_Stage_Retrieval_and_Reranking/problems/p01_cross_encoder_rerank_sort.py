"""Problem 01 — Cross Encoder Rerank Sort

Topic: 05 Multi Stage Retrieval and Reranking
Target: Production-grade implementation

Re-rank candidate documents using cross-encoder relevance scores and threshold.

Example:
    >>> cross_encoder_rerank_sort([("d1", 0.3), ("d2", 0.9), ("d3", 0.6)], 0.5)
    [('d2', 0.9), ('d3', 0.6)]

Hints:
    Hint 1: The first-stage retriever's original ordering is irrelevant
        here — only the cross-encoder score decides both which candidates
        survive and their final order.
    Hint 2: Filter with a comprehension keeping only entries where `score >=
        min_score_threshold`, then sort the survivors by score descending
        (`list.sort` with a key on the score and `reverse=True`).
    Hint 3: The threshold is inclusive — a score exactly equal to
        `min_score_threshold` passes, not just a strictly higher one — and
        filtering must remove low-score candidates regardless of the input
        list's original order, before or independent of the sort.
"""

from __future__ import annotations


def cross_encoder_rerank_sort(candidates: list[tuple[str, float]], min_score_threshold: float = 0.5) -> list[tuple[str, float]]:
    """candidates: list of (doc_id, score).
    Filter candidates with score >= min_score_threshold.
    Sort by score descending.
    Returns filtered, sorted list.
    """
    raise NotImplementedError("Implement cross_encoder_rerank_sort")
