"""Reference Solution — Problem 01: Maxsim Late Interaction

Topic: 06 ColBERTv2 and Late Interaction
"""

from __future__ import annotations


def maxsim_late_interaction(query_token_embeddings: list[list[float]], doc_token_embeddings: list[list[float]]) -> float:
    if not query_token_embeddings or not doc_token_embeddings:
        return 0.0
    total = 0.0
    for q in query_token_embeddings:
        max_dot = max(sum(qi * di for qi, di in zip(q, d)) for d in doc_token_embeddings)
        total += max_dot
    return round(total, 4)
