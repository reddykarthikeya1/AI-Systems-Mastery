"""Reference Solution — Problem 01: Reciprocal Rank Fusion Merge

Topic: 04 Hybrid Search and Reciprocal Rank Fusion
"""

from __future__ import annotations


def reciprocal_rank_fusion_merge(dense_ranked: list[str], sparse_ranked: list[str], k: int = 60) -> list[tuple[str, float]]:
    scores = {}
    for rank, doc in enumerate(dense_ranked, 1):
        scores[doc] = scores.get(doc, 0.0) + (1.0 / (k + rank))
    for rank, doc in enumerate(sparse_ranked, 1):
        scores[doc] = scores.get(doc, 0.0) + (1.0 / (k + rank))
    res = [(doc, round(sc, 5)) for doc, sc in scores.items()]
    res.sort(key=lambda x: x[1], reverse=True)
    return res
