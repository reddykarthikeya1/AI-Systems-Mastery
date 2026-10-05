#!/usr/bin/env python3
"""
===============================================================================
Hierarchical Navigable Small World (HNSW) Pure-Python Vector Index
===============================================================================
Metaphor:
  The Highway & Airplane Travel Analogy:
  - When traveling from New York to a quiet coffee shop in Los Angeles:
    - Layer 2 (Airplane): Fly from NYC to LAX (huge geographic jump).
    - Layer 1 (Highway): Drive from LAX along Interstate 10 into Santa Monica.
    - Layer 0 (Local Streets): Walk the last 200 feet to find the exact cafe.
  - HNSW does this in 1,536-dimensional space! Instead of computing distance to
    every document on Earth, it zooms in hierarchically in O(log N) time!
===============================================================================
"""

import math
import random
import heapq
import time
from typing import List, Dict, Tuple, Set


def euclidean_distance(v1: List[float], v2: List[float]) -> float:
    """Calculates L2 Euclidean distance between two vectors."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


class HNSWNode:
    def __init__(self, node_id: int, vector: List[float], level: int):
        self.id = node_id
        self.vector = vector
        self.level = level
        # Connections per level: {level_idx: set(neighbor_node_ids)}
        self.neighbors: Dict[int, Set[int]] = {lvl: set() for lvl in range(level + 1)}


class PurePythonHNSW:
    """
    Hierarchical Navigable Small World graph.
    Multi-layer approximate nearest neighbor search index.
    """
    def __init__(self, dim: int, max_elements: int = 5000, M: int = 8, ef_construction: int = 32, ml: float = 0.62):
        self.dim = dim
        self.M = M  # Max outgoing connections per node per layer
        self.ef_construction = ef_construction  # Size of dynamic candidate list
        self.ml = ml  # Normalization factor for level generation (1 / ln(M))
        
        self.nodes: Dict[int, HNSWNode] = {}
        self.entry_point_id: Optional[int] = None
        self.max_level = -1

    def _random_level(self) -> int:
        """Assigns a level using an exponential decay distribution (like Skip-List)."""
        r = random.random()
        if r == 0:
            r = 0.0000001
        lvl = int(-math.log(r) * self.ml)
        return min(lvl, 4)

    def insert(self, node_id: int, vector: List[float]) -> None:
        """Inserts a new vector node into the hierarchical graph."""
        level = self._random_level()
        new_node = HNSWNode(node_id, vector, level)
        self.nodes[node_id] = new_node

        if self.entry_point_id is None:
            self.entry_point_id = node_id
            self.max_level = level
            return

        curr_ep = self.entry_point_id

        # 1. Greedy search from top level down to level + 1
        for lvl in range(self.max_level, level, -1):
            curr_ep = self._search_layer_greedy(curr_ep, vector, lvl)

        # 2. From min(max_level, level) down to 0, find neighbors and link
        for lvl in range(min(self.max_level, level), -1, -1):
            candidates = self._search_layer_ef(curr_ep, vector, ef=self.ef_construction, level=lvl)
            # Pick M closest neighbors
            closest_m = [cand_id for dist, cand_id in candidates[:self.M]]

            for neighbor_id in closest_m:
                new_node.neighbors[lvl].add(neighbor_id)
                self.nodes[neighbor_id].neighbors[lvl].add(node_id)
                # Shrink neighbor's edge list if exceeding M
                if len(self.nodes[neighbor_id].neighbors[lvl]) > self.M:
                    self._prune_connections(neighbor_id, lvl)

            if closest_m:
                curr_ep = closest_m[0]

        if level > self.max_level:
            self.max_level = level
            self.entry_point_id = node_id

    def _search_layer_greedy(self, entry_id: int, query: List[float], level: int) -> int:
        """Finds closest node in a single layer using greedy routing."""
        curr = entry_id
        curr_dist = euclidean_distance(self.nodes[curr].vector, query)

        changed = True
        while changed:
            changed = False
            for neighbor_id in self.nodes[curr].neighbors.get(level, set()):
                d = euclidean_distance(self.nodes[neighbor_id].vector, query)
                if d < curr_dist:
                    curr_dist = d
                    curr = neighbor_id
                    changed = True
        return curr

    def _search_layer_ef(self, entry_id: int, query: List[float], ef: int, level: int) -> List[Tuple[float, int]]:
        """Bounded priority-queue search in a single layer returning top candidates."""
        visited = {entry_id}
        entry_dist = euclidean_distance(self.nodes[entry_id].vector, query)

        # candidates: min-heap of (dist, id) for unvisited exploration
        candidates = [(entry_dist, entry_id)]
        # results: max-heap of (-dist, id) keeping best ef items
        results = [(-entry_dist, entry_id)]

        while candidates:
            dist, current_id = heapq.heappop(candidates)
            worst_dist = -results[0][0]

            if dist > worst_dist and len(results) >= ef:
                break

            for neighbor_id in self.nodes[current_id].neighbors.get(level, set()):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    n_dist = euclidean_distance(self.nodes[neighbor_id].vector, query)
                    worst_dist = -results[0][0]

                    if n_dist < worst_dist or len(results) < ef:
                        heapq.heappush(candidates, (n_dist, neighbor_id))
                        heapq.heappush(results, (-n_dist, neighbor_id))
                        if len(results) > ef:
                            heapq.heappop(results)

        # Sort ascending by distance
        sorted_results = sorted([(-d, nid) for d, nid in results], key=lambda x: x[0])
        return sorted_results

    def _prune_connections(self, node_id: int, level: int) -> None:
        """Prunes outgoing connections to maintain bounded degree M."""
        node = self.nodes[node_id]
        nbrs = list(node.neighbors[level])
        # Sort by distance to node
        nbrs.sort(key=lambda nid: euclidean_distance(node.vector, self.nodes[nid].vector))
        node.neighbors[level] = set(nbrs[:self.M])

    def query(self, query_vec: List[float], k: int = 5, ef: int = 32) -> List[Tuple[int, float]]:
        """Queries the HNSW graph for top-K nearest neighbors."""
        if self.entry_point_id is None:
            return []

        curr_ep = self.entry_point_id
        # Traverse express layers greedily
        for lvl in range(self.max_level, 0, -1):
            curr_ep = self._search_layer_greedy(curr_ep, query_vec, lvl)

        # Base layer search with expanded ef budget
        candidates = self._search_layer_ef(curr_ep, query_vec, ef=max(ef, k), level=0)
        return [(cand_id, round(dist, 4)) for dist, cand_id in candidates[:k]]


# --- Production Verification & Recall Benchmark ---
def run_benchmark():
    print("=" * 70)
    print(" HNSW PURE PYTHON VECTOR INDEX BENCHMARK")
    print("=" * 70)

    DIMENSION = 16
    NUM_VECTORS = 1000
    K = 5
    random.seed(42)

    # Generate synthetic dataset
    print(f"[*] Generating {NUM_VECTORS:,} random vectors of dimension {DIMENSION}...")
    dataset = {i: [random.uniform(-1.0, 1.0) for _ in range(DIMENSION)] for i in range(NUM_VECTORS)}

    # Build HNSW Index
    print("[*] Building HNSW graph index...")
    hnsw = PurePythonHNSW(dim=DIMENSION, M=8, ef_construction=32)
    start_t = time.perf_counter()
    for vid, vec in dataset.items():
        hnsw.insert(vid, vec)
    build_time = time.perf_counter() - start_t
    print(f"    Built in {build_time:.2f}s (Max Graph Level reached: {hnsw.max_level})")

    # Pick a random query vector
    query_vector = [random.uniform(-1.0, 1.0) for _ in range(DIMENSION)]

    # 1. Ground Truth via Brute-Force O(N) Scan
    t0 = time.perf_counter()
    exact_all = sorted(
        [(vid, euclidean_distance(vec, query_vector)) for vid, vec in dataset.items()],
        key=lambda x: x[1]
    )
    exact_top_k = [(vid, round(dist, 4)) for vid, dist in exact_all[:K]]
    brute_time = time.perf_counter() - t0

    # 2. HNSW Search
    t1 = time.perf_counter()
    hnsw_top_k = hnsw.query(query_vector, k=K, ef=64)
    hnsw_time = time.perf_counter() - t1

    print("\n--- RESULTS COMPARISON ---")
    print("Ground Truth (Exact Brute-Force):")
    for r in exact_top_k:
        print(f"  Node ID {r[0]:4d} | Distance: {r[1]:.4f}")

    print("\nHNSW Approximate Nearest Neighbors:")
    for r in hnsw_top_k:
        print(f"  Node ID {r[0]:4d} | Distance: {r[1]:.4f}")

    exact_ids = {r[0] for r in exact_top_k}
    hnsw_ids = {r[0] for r in hnsw_top_k}
    recall = len(exact_ids.intersection(hnsw_ids)) / K

    print("-" * 70)
    print(f"Recall @ {K}               : {recall * 100:.1f}%")
    print(f"Brute Force Latency    : {brute_time * 1000:.3f} ms")
    print(f"HNSW Search Latency    : {hnsw_time * 1000:.3f} ms")
    assert recall >= 0.8, f"HNSW recall too low: {recall}"
    print("[PASS] HNSW graph index verified with high recall accuracy.")
    print("=" * 70)


if __name__ == "__main__":
    run_benchmark()
