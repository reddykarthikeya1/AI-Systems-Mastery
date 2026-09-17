"""Problem 01 — Jaccard Similarity Sets

Topic: 01 Set Language for Machine Learning
Target: Production-grade implementation

Compute Jaccard similarity and Jaccard distance between two categorical sets.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def jaccard_similarity_sets(set_a: set, set_b: set) -> tuple[float, float]:
    """Returns (similarity, distance) where:
    similarity = len(intersection) / len(union) if union else 1.0
    distance = 1.0 - similarity
    """
    raise NotImplementedError("Implement jaccard_similarity_sets")
