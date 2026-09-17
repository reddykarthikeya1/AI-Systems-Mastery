"""Problem 01 — Cosine Similarity Matrix

Topic: 03 Vector Database Internals
Target: Production-grade implementation

Compute cosine similarity between normalized vectors.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def cosine_similarity_matrix(v1: list[float], v2: list[float]) -> float:
    """Compute dot(v1, v2) / (norm(v1) * norm(v2)).
    Returns similarity rounded to 4 decimals (0.0 if either is zero vector).
    """
    raise NotImplementedError("Implement cosine_similarity_matrix")
