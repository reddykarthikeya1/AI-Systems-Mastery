"""Reference Solution — Problem 01: Cross Encoder Rerank Sort

Topic: 05 Multi Stage Retrieval and Reranking
"""

from __future__ import annotations


def cross_encoder_rerank_sort(candidates: list[tuple[str, float]], min_score_threshold: float = 0.5) -> list[tuple[str, float]]:
    filtered = [c for c in candidates if c[1] >= min_score_threshold]
    filtered.sort(key=lambda x: x[1], reverse=True)
    return filtered
