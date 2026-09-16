from __future__ import annotations

import heapq
import numpy as np


class SimpleHNSWIndex:
    """Simulates HNSW multi-layer graph navigation and approximate nearest neighbor search."""

    def __init__(self, dim: int, max_connections: int = 4):
        self.dim = dim
        self.m = max_connections
        self.vectors: dict[int, np.ndarray] = {}
        # Layer 1 (sparse highway) and Layer 0 (full base)
        self.layer_1_graph: dict[int, list[int]] = {}
        self.layer_0_graph: dict[int, list[int]] = {}
        self.entry_point: int | None = None

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        dot = np.dot(a, b)
        norm = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-9
        return float(dot / norm)

    def insert(self, node_id: int, vec: np.ndarray, is_highway: bool = False) -> None:
        self.vectors[node_id] = vec
        self.layer_0_graph[node_id] = []

        if self.entry_point is None:
            self.entry_point = node_id
            if is_highway:
                self.layer_1_graph[node_id] = []
            return

        # Connect in layer 0 to nearest existing nodes
        existing = [nid for nid in self.layer_0_graph if nid != node_id]
        if existing:
            sims = [(self.cosine_similarity(vec, self.vectors[nid]), nid) for nid in existing]
            sims.sort(reverse=True)
            neighbors = [nid for _, nid in sims[: self.m]]
            self.layer_0_graph[node_id] = list(neighbors)
            for n in neighbors:
                if len(self.layer_0_graph[n]) < self.m * 2:
                    self.layer_0_graph[n].append(node_id)

        if is_highway:
            self.layer_1_graph[node_id] = []
            hw_nodes = [nid for nid in self.layer_1_graph if nid != node_id]
            if hw_nodes:
                sims = [(self.cosine_similarity(vec, self.vectors[nid]), nid) for nid in hw_nodes]
                sims.sort(reverse=True)
                hw_neighbors = [nid for _, nid in sims[: self.m]]
                self.layer_1_graph[node_id] = list(hw_neighbors)
                for n in hw_neighbors:
                    self.layer_1_graph[n].append(node_id)

    def search_knn(self, query_vec: np.ndarray, k: int = 3) -> list[tuple[int, float]]:
        """Greedy search from highway layer down to layer 0."""
        if self.entry_point is None:
            return []

        curr = self.entry_point

        # Step 1: Greedy routing in Layer 1 if available
        if self.layer_1_graph:
            changed = True
            while changed:
                changed = False
                curr_sim = self.cosine_similarity(query_vec, self.vectors[curr])
                for neighbor in self.layer_1_graph.get(curr, []):
                    sim = self.cosine_similarity(query_vec, self.vectors[neighbor])
                    if sim > curr_sim:
                        curr = neighbor
                        curr_sim = sim
                        changed = True

        # Step 2: Search in Layer 0
        visited = {curr}
        candidates = [(-self.cosine_similarity(query_vec, self.vectors[curr]), curr)]
        best_results = [(self.cosine_similarity(query_vec, self.vectors[curr]), curr)]

        while candidates:
            neg_sim, node = heapq.heappop(candidates)
            for neighbor in self.layer_0_graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    sim = self.cosine_similarity(query_vec, self.vectors[neighbor])
                    heapq.heappush(candidates, (-sim, neighbor))
                    best_results.append((sim, neighbor))

        best_results.sort(reverse=True)
        return [(nid, round(sim, 4)) for sim, nid in best_results[:k]]
