"""Module 21: High-Scale Vector Database & HNSW Approximate Nearest Neighbor (ANN) Index.

Reference implementation of Hierarchical Navigable Small World (HNSW) graphs,
Scalar Quantization (SQ8), Cosine/Euclidean metrics, and metadata pre/post-filtering.

This is an **in-process model**, not a deployed distributed system. It runs in a
single Python process with no network, no separate nodes, and no real
infrastructure. That is the correct way to teach this material: you cannot spin
up a CDN, a global load balancer or a five-node consensus cluster inside a
lesson, and building the mechanism by hand is what makes it visible.

What that means for you: every algorithm and state transition here is real and
worth studying. The *operational* behaviour - partial network partitions, clock
skew across machines, kernel-level backpressure - is simulated, and the module
README says which parts are which.
"""

from __future__ import annotations

import heapq
import math
import random
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

# ============================================================================
# 1. Vector Distance Metrics
# ============================================================================

def euclidean_distance(v1: list[float], v2: list[float]) -> float:
    """Computes Euclidean (L2) distance between two dense vectors."""
    if len(v1) != len(v2):
        raise ValueError("Vector dimensionality mismatch")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2, strict=False)))


def cosine_distance(v1: list[float], v2: list[float]) -> float:
    """Computes Cosine distance (1 - cosine_similarity) in [0, 2]."""
    if len(v1) != len(v2):
        raise ValueError("Vector dimensionality mismatch")

    dot = sum(a * b for a, b in zip(v1, v2, strict=False))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))

    if norm1 == 0.0 or norm2 == 0.0:
        return 1.0  # Degenerate case

    similarity = dot / (norm1 * norm2)
    # Clamp to [-1.0, 1.0] to prevent floating point inaccuracies from yielding math domain errors
    similarity = max(-1.0, min(1.0, similarity))
    return 1.0 - similarity


# ============================================================================
# 2. Scalar Quantization (SQ8) Compression
# ============================================================================

@dataclass
class QuantizedVector:
    """Compressed 8-bit vector representation achieving 75% RAM reduction."""
    data: bytes
    min_val: float
    max_val: float
    dim: int


class ScalarQuantizer8:
    """Quantizes 32-bit floats into 8-bit unsigned integers [0, 255]."""

    @staticmethod
    def quantize(vector: list[float]) -> QuantizedVector:
        min_v = min(vector)
        max_v = max(vector)
        range_v = max_v - min_v

        if range_v == 0:
            return QuantizedVector(
                data=bytes([128] * len(vector)),
                min_val=min_v,
                max_val=max_v,
                dim=len(vector),
            )

        quantized = bytearray(len(vector))
        scale = 255.0 / range_v
        for i, val in enumerate(vector):
            q = round((val - min_v) * scale)
            quantized[i] = max(0, min(255, q))

        return QuantizedVector(
            data=bytes(quantized),
            min_val=min_v,
            max_val=max_v,
            dim=len(vector),
        )

    @staticmethod
    def dequantize(qv: QuantizedVector) -> list[float]:
        """Reconstructs approximate 32-bit float vector from 8-bit quantized bytes."""
        range_v = qv.max_val - qv.min_val
        if range_v == 0:
            return [qv.min_val] * qv.dim

        inv_scale = range_v / 255.0
        return [qv.min_val + b * inv_scale for b in qv.data]


# ============================================================================
# 3. Vector Records & Hybrid Metadata
# ============================================================================

@dataclass
class VectorRecord:
    doc_id: str
    vector: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(order=True)
class SearchCandidate:
    distance: float
    doc_id: str = field(compare=False)


# ============================================================================
# 4. HNSW Index Implementation
# ============================================================================

class HNSWIndex:
    """Hierarchical Navigable Small World (HNSW) proximity graph index."""

    def __init__(
        self,
        dim: int,
        metric: str = "cosine",
        M: int = 16,
        ef_construction: int = 32,
        ef_search: int = 16,
        random_seed: int | None = 42,
    ) -> None:
        self.dim = dim
        self.metric = metric
        self.M = M
        self.M0 = 2 * M  # Layer 0 can hold twice as many links
        self.ef_construction = ef_construction
        self.ef_search = ef_search
        self.m_L = 1.0 / math.log(M) if M > 1 else 1.0

        if random_seed is not None:
            self._rng = random.Random(random_seed)
        else:
            self._rng = random.Random()

        self._distance_fn: Callable[[list[float], list[float]], float]
        if metric == "cosine":
            self._distance_fn = cosine_distance
        elif metric == "euclidean":
            self._distance_fn = euclidean_distance
        else:
            raise ValueError(f"Unsupported metric: {metric}")

        # Document storage: doc_id -> VectorRecord
        self.nodes: dict[str, VectorRecord] = {}

        # Multi-layer graph representation: layer_idx -> { doc_id: Set[neighbor_id] }
        self.layers: list[dict[str, set[str]]] = []

        # Max level across all indexed nodes
        self.max_level: int = -1
        # Top-layer entry point doc_id
        self.entry_point: str | None = None

    def _get_distance(self, v1: list[float], v2: list[float]) -> float:
        return self._distance_fn(v1, v2)

    def _random_level(self) -> int:
        """Assigns maximum layer for a new node following exponential distribution."""
        unif = self._rng.random()
        while unif == 0.0:
            unif = self._rng.random()
        return math.floor(-math.log(unif) * self.m_L)

    def insert(self, doc_id: str, vector: list[float], metadata: dict[str, Any] | None = None) -> None:
        """Inserts a vector record into the multi-layer HNSW graph."""
        if len(vector) != self.dim:
            raise ValueError(f"Vector dim {len(vector)} does not match index dim {self.dim}")

        record = VectorRecord(doc_id=doc_id, vector=vector, metadata=metadata or {})
        self.nodes[doc_id] = record

        node_level = self._random_level()

        # Initialize layers up to node_level if needed
        while len(self.layers) <= max(node_level, self.max_level):
            self.layers.append({})

        # If index is empty, set as first entry point
        if self.entry_point is None:
            self.entry_point = doc_id
            self.max_level = node_level
            for lvl in range(node_level + 1):
                self.layers[lvl][doc_id] = set()
            return

        curr_obj = self.entry_point
        curr_dist = self._get_distance(vector, self.nodes[curr_obj].vector)

        # 1. Greedy search through higher layers (> node_level) to find closest entry point
        for lvl in range(self.max_level, node_level, -1):
            changed = True
            while changed:
                changed = False
                neighbors = self.layers[lvl].get(curr_obj, set())
                for neighbor in neighbors:
                    d = self._get_distance(vector, self.nodes[neighbor].vector)
                    if d < curr_dist:
                        curr_dist = d
                        curr_obj = neighbor
                        changed = True

        # 2. Insert from min(node_level, max_level) down to Layer 0
        top_insert_lvl = min(node_level, self.max_level)
        for lvl in range(top_insert_lvl, -1, -1):
            # Beam search on layer with beam width ef_construction
            candidates = self._search_layer(vector, [curr_obj], self.ef_construction, lvl)

            # Select M best neighbors (or M0 for layer 0)
            max_edges = self.M0 if lvl == 0 else self.M
            neighbors_to_connect = [c.doc_id for c in candidates[:max_edges]]

            # Initialize node in this layer
            if doc_id not in self.layers[lvl]:
                self.layers[lvl][doc_id] = set()

            for neighbor in neighbors_to_connect:
                self.layers[lvl][doc_id].add(neighbor)
                if neighbor not in self.layers[lvl]:
                    self.layers[lvl][neighbor] = set()
                self.layers[lvl][neighbor].add(doc_id)

                # Prune neighbor's outgoing edges if degree exceeds limit
                if len(self.layers[lvl][neighbor]) > max_edges:
                    self._prune_neighbors(neighbor, lvl, max_edges)

            if candidates:
                curr_obj = candidates[0].doc_id

        # 3. If new node level is higher than current max_level, establish new top layers
        if node_level > self.max_level:
            for lvl in range(self.max_level + 1, node_level + 1):
                self.layers[lvl][doc_id] = set()
            self.max_level = node_level
            self.entry_point = doc_id

    def _search_layer(
        self,
        query_vector: list[float],
        entry_points: list[str],
        ef: int,
        level: int
    ) -> list[SearchCandidate]:
        """Beam search exploring a single HNSW layer maintaining a candidate set."""
        visited: set[str] = set(entry_points)

        # Min-heap of candidates to explore: (distance, doc_id)
        candidates: list[tuple[float, str]] = []
        # Max-heap of nearest elements found: (-distance, doc_id)
        w_results: list[tuple[float, str]] = []

        for ep in entry_points:
            d = self._get_distance(query_vector, self.nodes[ep].vector)
            heapq.heappush(candidates, (d, ep))
            heapq.heappush(w_results, (-d, ep))

        while candidates:
            c_dist, c_id = heapq.heappop(candidates)
            furthest_dist = -w_results[0][0]

            if c_dist > furthest_dist:
                break

            neighbors = self.layers[level].get(c_id, set())
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    d = self._get_distance(query_vector, self.nodes[neighbor].vector)
                    furthest_dist = -w_results[0][0]

                    if d < furthest_dist or len(w_results) < ef:
                        heapq.heappush(candidates, (d, neighbor))
                        heapq.heappush(w_results, (-d, neighbor))
                        if len(w_results) > ef:
                            heapq.heappop(w_results)

        # Convert w_results (max-heap) to sorted ascending list of SearchCandidate
        res = [SearchCandidate(distance=-neg_d, doc_id=doc_id) for neg_d, doc_id in w_results]
        res.sort(key=lambda x: x.distance)
        return res

    def _prune_neighbors(self, node_id: str, level: int, max_edges: int) -> None:
        """Prunes outgoing edges of a node to maintain graph sparsity."""
        neighbors = list(self.layers[level].get(node_id, set()))
        if len(neighbors) <= max_edges:
            return

        node_vec = self.nodes[node_id].vector
        scored = [
            (self._get_distance(node_vec, self.nodes[n].vector), n)
            for n in neighbors
        ]
        scored.sort(key=lambda x: x[0])
        self.layers[level][node_id] = {n for _, n in scored[:max_edges]}

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
        filter_predicate: Callable[[dict[str, Any]], bool] | None = None,
    ) -> list[tuple[str, float, dict[str, Any]]]:
        """Searches top-k approximate nearest neighbors with optional hybrid metadata filtering."""
        if not self.entry_point or self.max_level < 0:
            return []

        curr_obj = self.entry_point
        curr_dist = self._get_distance(query_vector, self.nodes[curr_obj].vector)

        # 1. Greedy routing down to Layer 1
        for lvl in range(self.max_level, 0, -1):
            changed = True
            while changed:
                changed = False
                neighbors = self.layers[lvl].get(curr_obj, set())
                for neighbor in neighbors:
                    d = self._get_distance(query_vector, self.nodes[neighbor].vector)
                    if d < curr_dist:
                        curr_dist = d
                        curr_obj = neighbor
                        changed = True

        # 2. Beam search at Layer 0 with ef_search
        ef = max(self.ef_search, top_k)
        candidates = self._search_layer(query_vector, [curr_obj], ef=ef, level=0)

        # 3. Apply hybrid metadata filter
        results = []
        for cand in candidates:
            record = self.nodes[cand.doc_id]
            if filter_predicate is None or filter_predicate(record.metadata):
                results.append((cand.doc_id, cand.distance, record.metadata))
                if len(results) >= top_k:
                    break

        return results


# ============================================================================
# 5. Exact Flat Index (Ground Truth for Measuring ANN Recall)
# ============================================================================

class BruteForceFlatIndex:
    """Exact flat index used to benchmark HNSW recall rate."""

    def __init__(self, metric: str = "cosine") -> None:
        self.records: dict[str, VectorRecord] = {}
        self.distance_fn = cosine_distance if metric == "cosine" else euclidean_distance

    def insert(self, doc_id: str, vector: list[float], metadata: dict[str, Any] | None = None) -> None:
        self.records[doc_id] = VectorRecord(doc_id=doc_id, vector=vector, metadata=metadata or {})

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
        filter_predicate: Callable[[dict[str, Any]], bool] | None = None,
    ) -> list[tuple[str, float, dict[str, Any]]]:
        candidates = []
        for doc_id, rec in self.records.items():
            if filter_predicate and not filter_predicate(rec.metadata):
                continue
            d = self.distance_fn(query_vector, rec.vector)
            candidates.append((doc_id, d, rec.metadata))

        candidates.sort(key=lambda x: x[1])
        return candidates[:top_k]
