"""Problem 01 — Maxsim Late Interaction

Topic: 06 ColBERTv2 and Late Interaction
Target: Production-grade implementation

Compute ColBERT MaxSim operator between query and document token embeddings.

Example:
    >>> maxsim_late_interaction([[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.5, 0.5]])
    1.5

Hints:
    Hint 1: ColBERT keeps every token's own embedding instead of pooling
        into one vector, so each QUERY token independently picks its own
        best-matching document token — different query tokens can align to
        different doc tokens.
    Hint 2: Nested iteration: for each query token embedding, compute its
        dot product against every document token embedding and take the
        max, then sum those per-query-token maxima across all query tokens.
    Hint 3: An empty `query_token_embeddings` or `doc_token_embeddings` must
        return 0.0 rather than raising on an empty `max()`; the final sum is
        rounded to 4 decimals; and the operation order matters — it's
        max-then-sum over query tokens, never sum-then-max or an average.
"""

from __future__ import annotations


def maxsim_late_interaction(query_token_embeddings: list[list[float]], doc_token_embeddings: list[list[float]]) -> float:
    """For each query token embedding q, find max dot product with all doc token embeddings d.
    MaxSim = sum_q (max_d (dot(q, d))).
    Returns MaxSim score rounded to 4 decimals.
    """
    raise NotImplementedError("Implement maxsim_late_interaction")
