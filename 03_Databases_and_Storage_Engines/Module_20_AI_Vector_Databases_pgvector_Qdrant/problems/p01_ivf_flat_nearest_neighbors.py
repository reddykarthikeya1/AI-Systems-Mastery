"""Problem 01 — Ivf Flat Nearest Neighbors

Topic: 20 AI Vector Databases pgvector Qdrant
Target: Production-grade implementation

Search IVF-Flat vector clusters for nearest neighbors.

Example:
    >>> centroids = [[0.0, 0.0], [10.0, 10.0]]
    >>> clusters = {
    ...     0: [(1, [0.1, 0.1]), (2, [0.2, 0.2])],
    ...     1: [(3, [9.9, 9.9]), (4, [10.1, 10.1])],
    ... }
    >>> ivf_flat_nearest_neighbors([0.05, 0.05], centroids, clusters, nprobe=1)
    [1, 2]

Hints:
    Hint 1: This is a two-stage, coarse-then-fine search — you never touch
        every vector, only the ones living inside the handful of clusters
        whose centroid is closest to the query.
    Hint 2: First rank all centroids by (squared) Euclidean distance to
        query_vec and keep the nprobe closest cluster ids; then flatten only
        those clusters' (id, vector) pairs, rank them the same way, and keep
        the 3 nearest.
    Hint 3: Squared distance (skip the sqrt) is enough since only relative
        ordering matters; sort each stage as (distance, id) tuples so ties
        break on id predictably, and when fewer than 3 candidates exist
        across the probed clusters, return however many there are rather
        than padding or raising.
"""

from __future__ import annotations


def ivf_flat_nearest_neighbors(query_vec: list[float], centroids: list[list[float]], clusters: dict[int, list[tuple[int, list[float]]]], nprobe: int = 2) -> list[int]:
    """1. Find nprobe closest centroid indices by Euclidean distance to query_vec.
    2. Scan all vectors in those chosen clusters and return top 3 vector IDs closest to query_vec.
    """
    raise NotImplementedError("Implement ivf_flat_nearest_neighbors")
