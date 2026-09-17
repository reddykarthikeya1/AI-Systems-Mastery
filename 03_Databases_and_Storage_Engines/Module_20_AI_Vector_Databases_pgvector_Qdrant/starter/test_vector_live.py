"""Tests for Module 20: Real Vector DBs - Qdrant & pgvector (Track B).

Validates:
1. QdrantLiveClient connection & health ping (runs in-process via :memory:)
2. Vector collection creation with Cosine distance metric
3. Upserting multi-dimensional vector embeddings with metadata payload
4. Filtered ANN similarity search combining vector distance + scalar filters
5. RECONCILIATION: Handbuilt VectorMetrics cosine distance matches vector alignment
6. RECONCILIATION: Handbuilt FlatVectorIndex top-k ranking matches Qdrant in-memory ranking
"""

from __future__ import annotations

import pytest

from Module_20_AI_Vector_Databases_pgvector_Qdrant.project_solution.vector_live import QdrantLiveClient
from Module_20_AI_Vector_Databases_pgvector_Qdrant.project_solution.vector_engine import (
    VectorMetrics as HandbuiltMetrics,
    FlatVectorIndex as HandbuiltFlatIndex,
    VectorItem as HandbuiltItem,
)


# --- IN-PROCESS RECONCILIATION & LIVE QDRANT IN-MEMORY TESTS ---

def test_reconciliation_cosine_distance():
    """Verify handbuilt cosine distance is 0.0 for identical vectors and 1.0 for orthogonal vectors."""
    u = [1.0, 0.0, 0.0]
    v = [1.0, 0.0, 0.0]
    w = [0.0, 1.0, 0.0]

    # Identical vectors: distance is 0
    assert pytest.approx(HandbuiltMetrics.cosine_distance(u, v), abs=1e-5) == 0.0

    # Orthogonal vectors: cosine similarity is 0 -> distance is 1.0
    assert pytest.approx(HandbuiltMetrics.cosine_distance(u, w), abs=1e-5) == 1.0


def test_reconciliation_top_k_ranking_with_qdrant():
    """Verify handbuilt brute-force index and real Qdrant in-memory client yield the same top neighbor."""
    # 1. Populate handbuilt flat index
    flat_idx = HandbuiltFlatIndex()
    flat_idx.add(HandbuiltItem("item_1", [1.0, 0.0, 0.0], {"category": "A"}))
    flat_idx.add(HandbuiltItem("item_2", [0.8, 0.2, 0.0], {"category": "A"}))
    flat_idx.add(HandbuiltItem("item_3", [0.0, 1.0, 0.0], {"category": "B"}))

    handbuilt_results = flat_idx.search(query_vec=[1.0, 0.0, 0.0], top_k=2)
    assert handbuilt_results[0][0].item_id == "item_1"
    assert handbuilt_results[1][0].item_id == "item_2"

    # 2. Populate real Qdrant in-memory client
    client = QdrantLiveClient(location=":memory:")
    assert client.ping() is True
    client.create_collection("bench_col", dim=3, distance="Cosine")
    client.upsert_vectors("bench_col", [
        (1, [1.0, 0.0, 0.0], {"category": "A"}),
        (2, [0.8, 0.2, 0.0], {"category": "A"}),
        (3, [0.0, 1.0, 0.0], {"category": "B"}),
    ])

    qdrant_results = client.search_similar("bench_col", query_vector=[1.0, 0.0, 0.0], top_k=2)
    assert qdrant_results[0]["id"] == 1
    assert qdrant_results[1]["id"] == 2


def test_qdrant_live_filtered_search():
    """Verify Qdrant in-memory search respects metadata payload filters."""
    client = QdrantLiveClient(location=":memory:")
    client.create_collection("filtered_col", dim=3, distance="Cosine")
    client.upsert_vectors("filtered_col", [
        (101, [0.9, 0.1, 0.0], {"category": "finance"}),
        (102, [0.95, 0.05, 0.0], {"category": "engineering"}),
    ])

    # Search with filter for 'finance': point 101 must match even if 102 was slightly closer
    res = client.search_similar(
        "filtered_col",
        query_vector=[1.0, 0.0, 0.0],
        top_k=2,
        filter_category="finance",
    )
    assert len(res) == 1
    assert res[0]["id"] == 101
    assert res[0]["payload"]["category"] == "finance"
