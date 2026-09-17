"""Reference Solution — Problem 01: Ivf Flat Nearest Neighbors

Topic: 20 AI Vector Databases pgvector Qdrant
"""

from __future__ import annotations


def ivf_flat_nearest_neighbors(query_vec: list[float], centroids: list[list[float]], clusters: dict[int, list[tuple[int, list[float]]]], nprobe: int = 2) -> list[int]:
    def dist(a: list[float], b: list[float]) -> float:
        return sum((x - y) ** 2 for x, y in zip(a, b))
    
    # Find closest centroids
    c_dists = [(dist(query_vec, c), i) for i, c in enumerate(centroids)]
    c_dists.sort()
    chosen_clusters = [i for _, i in c_dists[:nprobe]]
    
    # Search within clusters
    candidates = []
    for c_id in chosen_clusters:
        for vid, vec in clusters.get(c_id, []):
            candidates.append((dist(query_vec, vec), vid))
    candidates.sort()
    return [vid for _, vid in candidates[:3]]
