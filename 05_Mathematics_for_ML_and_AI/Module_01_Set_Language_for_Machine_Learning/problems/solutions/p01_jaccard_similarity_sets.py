"""Reference Solution — Problem 01: Jaccard Similarity Sets

Topic: 01 Set Language for Machine Learning
"""

from __future__ import annotations


def jaccard_similarity_sets(set_a: set, set_b: set) -> tuple[float, float]:
    u = set_a | set_b
    if not u:
        return (1.0, 0.0)
    sim = len(set_a & set_b) / len(u)
    return (round(sim, 4), round(1.0 - sim, 4))
