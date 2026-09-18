"""Problem 01 — Cosine Similarity Matrix

Topic: 03 Vector Database Internals
Target: Production-grade implementation

Compute cosine similarity between normalized vectors.

Example:
    >>> cosine_similarity_matrix([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])
    0.9746

Hints:
    Hint 1: Cosine similarity only cares about the ANGLE between the two
        vectors, not their magnitude, so you need the dot product and each
        vector's own length as separate quantities.
    Hint 2: Compute `dot = sum(x * y for x, y in zip(v1, v2))` and each
        Euclidean norm with `math.sqrt(sum(x * x for x in v))`, then divide
        the dot product by the product of the two norms.
    Hint 3: A zero vector makes the denominator zero, which must return
        `0.0` instead of raising `ZeroDivisionError` — check both norms
        before dividing — and the final similarity must be rounded to
        exactly 4 decimal places.
"""

from __future__ import annotations


def cosine_similarity_matrix(v1: list[float], v2: list[float]) -> float:
    """Compute dot(v1, v2) / (norm(v1) * norm(v2)).
    Returns similarity rounded to 4 decimals (0.0 if either is zero vector).
    """
    raise NotImplementedError("Implement cosine_similarity_matrix")
