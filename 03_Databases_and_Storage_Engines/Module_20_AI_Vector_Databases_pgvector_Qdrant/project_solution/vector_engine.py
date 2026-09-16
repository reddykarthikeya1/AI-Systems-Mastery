"""Module 20: AI Vector Databases, Distance Metrics & HNSW Engine (Solution).

This is a pure-Python MODEL of vector similarity search, IVFFlat, and HNSW graph indexing, built to make the
mechanism visible. It does not connect to pgvector or Qdrant. For the real driver,
real queries and real operational behaviour, see `pgvector_live.py` and `qdrant_live.py`.

Implements:
1. VectorMetrics: Cosine distance, Euclidean distance, and Dot Product.
2. FlatVectorIndex: Exact brute-force k-NN index.
3. HNSWIndex: Hierarchical Navigable Small World graph with multi-layer greedy routing.
4. Metadata payload filtering and ANN recall evaluation.
"""

from __future__ import annotations

import math
import random
from typing import Any


class VectorItem:
    """A vector embedding with unique identifier and metadata payload."""

    def __init__(self, item_id: str, vector: list[float], payload: dict[str, Any] | None = None) -> None:
        self.item_id = item_id
        self.vector = list(vector)
        self.payload = dict(payload or {})

    def __repr__(self) -> str:
        return f"VectorItem(id={self.item_id}, payload={self.payload})"


class VectorMetrics:
    """Mathematical vector distance functions."""

    @staticmethod
    def cosine_distance(u: list[float], v: list[float]) -> float:
        dot = sum(a * b for a, b in zip(u, v))
        norm_u = math.sqrt(sum(a * a for a in u))
        norm_v = math.sqrt(sum(b * b for b in v))
        if norm_u == 0.0 or norm_v == 0.0:
            return 1.0
        similarity = dot / (norm_u * norm_v)
        return max(0.0, 1.0 - similarity)

    @staticmethod
    def euclidean_distance(u: list[float], v: list[float]) -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(u, v)))

    @staticmethod
    def dot_product(u: list[float], v: list[float]) -> float:
        return sum(a * b for a, b in zip(u, v))


class FlatVectorIndex:
    """Exact brute-force k-NN index serving as ground truth baseline."""

    def __init__(self) -> None:
        self.items: list[VectorItem] = []

    def add(self, item: VectorItem) -> None:
        self.items.append(item)

    def search(
        self,
        query_vec: list[float],
        top_k: int = 5,
        filter_payload: dict[str, Any] | None = None,
    ) -> list[tuple[VectorItem, float]]:
        scored: list[tuple[VectorItem, float]] = []

        for item in self.items:
            if filter_payload is not None:
                matches = all(item.payload.get(k) == v for k, v in filter_payload.items())
                if not matches:
                    continue

            dist = VectorMetrics.cosine_distance(item.vector, query_vec)
            scored.append((item, dist))

        scored.sort(key=lambda x: x[1])
        return scored[:top_k]


class HNSWIndex:
    """Hierarchical Navigable Small World (HNSW) Approximate Nearest Neighbor index."""

    def __init__(
        self,
        m: int = 4,
        ef_construction: int = 16,
        ef_search: int = 8,
        max_layers: int = 4,
    ) -> None:
        self.m = m
        self.ef_construction = ef_construction
        self.ef_search = ef_search
        self.max_layers = max_layers

        # List of layer dicts: layer_idx -> {node_id: [neighbor_node_ids]}
        self.layers: list[dict[str, list[str]]] = [{} for _ in range(max_layers)]
        self.items: dict[str, VectorItem] = {}
        self.entry_point: str | None = None
        self.max_level: int = 0

    def _assign_level(self) -> int:
        # Probabilistic level generation (geometric distribution)
        lvl = 0
        while random.random() < 0.5 and lvl < self.max_layers - 1:
            lvl += 1
        return lvl

    def _greedy_search_layer(self, entry_id: str, query_vec: list[float], layer: int) -> str:
        curr = entry_id
        curr_dist = VectorMetrics.cosine_distance(self.items[curr].vector, query_vec)

        changed = True
        while changed:
            changed = False
            for neighbor_id in self.layers[layer].get(curr, []):
                dist = VectorMetrics.cosine_distance(self.items[neighbor_id].vector, query_vec)
                if dist < curr_dist:
                    curr_dist = dist
                    curr = neighbor_id
                    changed = True

        return curr

    def _search_layer_candidates(
        self,
        entry_id: str,
        query_vec: list[float],
        ef: int,
        layer: int,
    ) -> list[tuple[str, float]]:
        entry_dist = VectorMetrics.cosine_distance(self.items[entry_id].vector, query_vec)
        visited: set[str] = {entry_id}
        candidates: list[tuple[str, float]] = [(entry_id, entry_dist)]
        results: list[tuple[str, float]] = [(entry_id, entry_dist)]

        while candidates:
            candidates.sort(key=lambda x: x[1])
            closest_id, closest_dist = candidates.pop(0)

            # Pruning condition: if closest candidate is worse than furthest in results and len >= ef
            if len(results) >= ef and closest_dist > max(r[1] for r in results):
                break

            for neighbor_id in self.layers[layer].get(closest_id, []):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    dist = VectorMetrics.cosine_distance(self.items[neighbor_id].vector, query_vec)

                    if len(results) < ef or dist < max(r[1] for r in results):
                        candidates.append((neighbor_id, dist))
                        results.append((neighbor_id, dist))
                        results.sort(key=lambda x: x[1])
                        if len(results) > ef:
                            results.pop()

        results.sort(key=lambda x: x[1])
        return results

    def _prune_neighbors(self, node_id: str, neighbors: list[str], max_m: int) -> list[str]:
        target_vec = self.items[node_id].vector
        scored = [
            (nid, VectorMetrics.cosine_distance(self.items[nid].vector, target_vec))
            for nid in neighbors
        ]
        scored.sort(key=lambda x: x[1])
        return [nid for nid, _ in scored[:max_m]]

    def add(self, item: VectorItem) -> None:
        item_id = item.item_id
        self.items[item_id] = item

        if self.entry_point is None:
            self.entry_point = item_id
            for layer_idx in range(self.max_layers):
                self.layers[layer_idx][item_id] = []
            return

        target_level = self._assign_level()
        curr_node = self.entry_point

        # Phase 1: Greedy traversal down to target_level
        for layer_idx in range(self.max_level, target_level, -1):
            curr_node = self._greedy_search_layer(curr_node, item.vector, layer_idx)

        # Phase 2: Connect at levels target_level down to 0
        top_conn_level = min(self.max_level, target_level)
        for layer_idx in range(top_conn_level, -1, -1):
            candidates = self._search_layer_candidates(
                curr_node, item.vector, ef=self.ef_construction, layer=layer_idx
            )
            selected = [nid for nid, _ in candidates[:self.m]]
            self.layers[layer_idx][item_id] = selected

            for n in selected:
                if item_id not in self.layers[layer_idx][n]:
                    self.layers[layer_idx][n].append(item_id)
                    if len(self.layers[layer_idx][n]) > self.m:
                        self.layers[layer_idx][n] = self._prune_neighbors(n, self.layers[layer_idx][n], self.m)

            if candidates:
                curr_node = candidates[0][0]

        for layer_idx in range(target_level + 1):
            if item_id not in self.layers[layer_idx]:
                self.layers[layer_idx][item_id] = []

        if target_level > self.max_level:
            self.max_level = target_level
            self.entry_point = item_id

    def search(
        self,
        query_vec: list[float],
        top_k: int = 5,
        filter_payload: dict[str, Any] | None = None,
    ) -> list[tuple[VectorItem, float]]:
        if not self.items or self.entry_point is None:
            return []

        curr_node = self.entry_point
        # Greedy routing through upper layers
        for layer_idx in range(self.max_level, 0, -1):
            curr_node = self._greedy_search_layer(curr_node, query_vec, layer_idx)

        # Beam search at Layer 0
        candidates = self._search_layer_candidates(
            curr_node, query_vec, ef=max(self.ef_search, top_k * 3), layer=0
        )

        results: list[tuple[VectorItem, float]] = []
        for nid, dist in candidates:
            item = self.items[nid]
            if filter_payload is not None:
                matches = all(item.payload.get(k) == v for k, v in filter_payload.items())
                if not matches:
                    continue

            results.append((item, dist))
            if len(results) == top_k:
                break

        return results
