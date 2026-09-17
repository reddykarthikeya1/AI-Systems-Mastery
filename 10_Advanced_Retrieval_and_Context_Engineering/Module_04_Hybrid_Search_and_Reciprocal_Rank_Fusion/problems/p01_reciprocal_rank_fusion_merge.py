"""Problem 01 — Reciprocal Rank Fusion Merge

Topic: 04 Hybrid Search and Reciprocal Rank Fusion
Target: Production-grade implementation

Combine dense and sparse ranked lists using Reciprocal Rank Fusion (RRF).

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def reciprocal_rank_fusion_merge(dense_ranked: list[str], sparse_ranked: list[str], k: int = 60) -> list[tuple[str, float]]:
    """RRF score for doc d: sum(1.0 / (k + rank)) across both lists (1-based rank).
    Returns list of (doc_id, rrf_score) sorted by rrf_score descending.
    """
    raise NotImplementedError("Implement reciprocal_rank_fusion_merge")
