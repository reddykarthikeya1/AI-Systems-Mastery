"""Problem 01 — Maxsim Late Interaction

Topic: 06 ColBERTv2 and Late Interaction
Target: Production-grade implementation

Compute ColBERT MaxSim operator between query and document token embeddings.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def maxsim_late_interaction(query_token_embeddings: list[list[float]], doc_token_embeddings: list[list[float]]) -> float:
    """For each query token embedding q, find max dot product with all doc token embeddings d.
    MaxSim = sum_q (max_d (dot(q, d))).
    Returns MaxSim score rounded to 4 decimals.
    """
    raise NotImplementedError("Implement maxsim_late_interaction")
