"""Microsoft DiskANN Vamana Graph Indexing Algorithm Simulator."""

from __future__ import annotations

import math
from typing import Dict, List, Set


def euclidean_distance(v1: List[float], v2: List[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


class VamanaGraphIndexer:
    """DiskANN Vamana graph indexing algorithm with alpha-pruning."""

    def __init__(self, max_out_degree: int = 4, alpha: float = 1.2) -> None:
        self.max_out_degree = max_out_degree
        self.alpha = alpha
        self.vectors: Dict[str, List[float]] = {}
        self.graph: Dict[str, Set[str]] = {}

    def insert(self, node_id: str, vector: List[float]) -> None:
        self.vectors[node_id] = vector
        self.graph[node_id] = set()

    def robust_prune(self, candidate_ids: List[str], current_node_id: str) -> Set[str]:
        """Alpha-pruning algorithm: preserves long-range shortcuts while bounding degree."""
        curr_vec = self.vectors[current_node_id]
        sorted_candidates = sorted(
            [c for c in candidate_ids if c != current_node_id],
            key=lambda cid: euclidean_distance(self.vectors[cid], curr_vec),
        )

        pruned_neighbors: Set[str] = set()

        for p in sorted_candidates:
            if len(pruned_neighbors) >= self.max_out_degree:
                break
            p_vec = self.vectors[p]

            should_add = True
            dist_p_curr = euclidean_distance(p_vec, curr_vec)
            for r in pruned_neighbors:
                dist_p_r = euclidean_distance(p_vec, self.vectors[r])
                if dist_p_curr > self.alpha * dist_p_r:
                    should_add = False
                    break

            if should_add:
                pruned_neighbors.add(p)

        return pruned_neighbors

    def build_index(self) -> None:
        """Connects nodes using robust pruning."""
        all_ids = list(self.vectors.keys())
        for node_id in all_ids:
            self.graph[node_id] = self.robust_prune(all_ids, node_id)
