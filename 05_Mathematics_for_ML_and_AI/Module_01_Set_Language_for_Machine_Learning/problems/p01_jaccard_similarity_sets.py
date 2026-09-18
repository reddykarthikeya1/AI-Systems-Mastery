"""Problem 01 — Jaccard Similarity Sets

Topic: 01 Set Language for Machine Learning
Target: Production-grade implementation

Compute Jaccard similarity and Jaccard distance between two categorical sets.

Example:
    >>> jaccard_similarity_sets({'a', 'b', 'c'}, {'b', 'c', 'd'})
    (0.5, 0.5)

Hints:
    Hint 1: Both quantities come from just two numbers: the size of the
        intersection and the size of the union — everything else follows.
    Hint 2: Build the union with `|` and the intersection with `&`, then
        divide `len(intersection) / len(union)` to get the similarity, and
        subtract from 1.0 for the distance.
    Hint 3: Two empty sets give an empty union, which would divide by zero;
        the spec defines that special case as similarity 1.0 (identical,
        vacuously) and distance 0.0. Round both results to 4 decimal places.
"""

from __future__ import annotations


def jaccard_similarity_sets(set_a: set, set_b: set) -> tuple[float, float]:
    """Returns (similarity, distance) where:
    similarity = len(intersection) / len(union) if union else 1.0
    distance = 1.0 - similarity
    """
    raise NotImplementedError("Implement jaccard_similarity_sets")
