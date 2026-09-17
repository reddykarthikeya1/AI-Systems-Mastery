"""Problem 01 — Ivf Flat Nearest Neighbors

Topic: 20 AI Vector Databases pgvector Qdrant
Target: Production-grade implementation

Search IVF-Flat vector clusters for nearest neighbors.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def ivf_flat_nearest_neighbors(query_vec: list[float], centroids: list[list[float]], clusters: dict[int, list[tuple[int, list[float]]]], nprobe: int = 2) -> list[int]:
    """1. Find nprobe closest centroid indices by Euclidean distance to query_vec.
    2. Scan all vectors in those chosen clusters and return top 3 vector IDs closest to query_vec.
    """
    raise NotImplementedError("Implement ivf_flat_nearest_neighbors")
