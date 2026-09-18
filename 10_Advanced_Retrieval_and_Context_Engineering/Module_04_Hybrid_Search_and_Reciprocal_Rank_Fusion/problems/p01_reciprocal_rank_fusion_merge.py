"""Problem 01 — Reciprocal Rank Fusion Merge

Topic: 04 Hybrid Search and Reciprocal Rank Fusion
Target: Production-grade implementation

Combine dense and sparse ranked lists using Reciprocal Rank Fusion (RRF).

Example:
    >>> reciprocal_rank_fusion_merge(["docA", "docB"], ["docB", "docC"], 60)
    [('docB', 0.03252), ('docA', 0.01639), ('docC', 0.01613)]

Hints:
    Hint 1: RRF deliberately ignores the raw retrieval scores and works only
        from RANK position; a document's fused score is the SUM of its
        contributions from every list it shows up in.
    Hint 2: Accumulate scores in a dict keyed by doc_id: walk each ranked
        list with `enumerate(..., 1)` for 1-based ranks, adding `1.0 / (k +
        rank)` into that doc's running total, then sort the resulting
        `(doc_id, score)` pairs by score descending.
    Hint 3: A document in both lists must have both contributions ADDED
        together, not maxed or overwritten; a document missing from one
        list simply gets no contribution from it (no default rank to
        assume); and the score must be rounded (5 decimals) before the
        descending sort the tests check.
"""

from __future__ import annotations


def reciprocal_rank_fusion_merge(dense_ranked: list[str], sparse_ranked: list[str], k: int = 60) -> list[tuple[str, float]]:
    """RRF score for doc d: sum(1.0 / (k + rank)) across both lists (1-based rank).
    Returns list of (doc_id, rrf_score) sorted by rrf_score descending.
    """
    raise NotImplementedError("Implement reciprocal_rank_fusion_merge")
