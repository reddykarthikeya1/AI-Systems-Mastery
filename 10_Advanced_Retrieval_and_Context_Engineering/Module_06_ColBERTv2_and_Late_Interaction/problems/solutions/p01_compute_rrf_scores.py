"""Reference Solution — Problem 01: compute_rrf_scores

Topic: ColBERTv2 and Late Interaction
"""

from __future__ import annotations

def compute_rrf_scores(rank_lists: list[list[str]], k: int = 60) -> dict[str, float]:
    scores: dict[str, float] = {}
    for rlist in rank_lists:
        for rank, doc_id in enumerate(rlist, 1):
            scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank))
    return {doc: round(score, 6) for doc, score in sorted(scores.items(), key=lambda item: item[1], reverse=True)}

