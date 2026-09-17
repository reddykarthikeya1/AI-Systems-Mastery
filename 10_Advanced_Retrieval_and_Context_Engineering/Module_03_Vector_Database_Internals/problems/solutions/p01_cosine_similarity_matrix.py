"""Reference Solution — Problem 01: Cosine Similarity Matrix

Topic: 03 Vector Database Internals
"""

from __future__ import annotations


def cosine_similarity_matrix(v1: list[float], v2: list[float]) -> float:
    import math
    dot = sum(x * y for x, y in zip(v1, v2))
    n1 = math.sqrt(sum(x * x for x in v1))
    n2 = math.sqrt(sum(y * y for y in v2))
    if n1 == 0 or n2 == 0:
        return 0.0
    return round(dot / (n1 * n2), 4)
