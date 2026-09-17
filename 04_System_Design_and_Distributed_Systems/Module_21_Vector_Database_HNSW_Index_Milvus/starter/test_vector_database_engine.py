"""Unit and integration test suite for Module 21: Vector Database & HNSW Indexing."""

import random

import pytest
from vector_database_engine import (
    BruteForceFlatIndex,
    HNSWIndex,
    ScalarQuantizer8,
    cosine_distance,
    euclidean_distance,
)


def test_distance_metrics() -> None:
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    v3 = [0.0, 1.0, 0.0]

    # Identical vectors: distance should be 0.0
    assert cosine_distance(v1, v2) == pytest.approx(0.0, abs=1e-5)
    assert euclidean_distance(v1, v2) == pytest.approx(0.0, abs=1e-5)

    # Orthogonal vectors: cosine distance is 1.0 (since similarity is 0.0)
    assert cosine_distance(v1, v3) == pytest.approx(1.0, abs=1e-5)
    assert euclidean_distance(v1, v3) == pytest.approx(1.41421356, abs=1e-4)

    # Dimension mismatch
    with pytest.raises(ValueError):
        cosine_distance([1.0], [1.0, 2.0])


def test_scalar_quantization_sq8() -> None:
    vec = [0.1, -0.5, 1.2, 3.4, -2.1]
    qv = ScalarQuantizer8.quantize(vec)

    assert len(qv.data) == len(vec)
    assert qv.dim == len(vec)

    # Dequantized reconstruction should have low error
    reconstructed = ScalarQuantizer8.dequantize(qv)
    for orig, rec in zip(vec, reconstructed, strict=False):
        assert abs(orig - rec) < 0.05  # Within 8-bit resolution error


def test_hnsw_insertion_and_graph_properties() -> None:
    dim = 8
    hnsw = HNSWIndex(dim=dim, metric="euclidean", M=4, random_seed=42)

    for i in range(25):
        vec = [float(i + j) for j in range(dim)]
        hnsw.insert(f"doc_{i}", vec, metadata={"idx": i})

    assert hnsw.entry_point is not None
    assert hnsw.max_level >= 0
    assert len(hnsw.nodes) == 25

    # Check maximum degree constraint across layers
    for lvl in range(1, hnsw.max_level + 1):
        for _node_id, neighbors in hnsw.layers[lvl].items():
            # Outgoing links should be bounded by M
            assert len(neighbors) <= hnsw.M + 1  # Allowing small boundary margin during edge linking


def test_hnsw_search_and_recall_vs_flat() -> None:
    dim = 8
    rng = random.Random(123)
    hnsw = HNSWIndex(dim=dim, metric="cosine", M=8, ef_construction=32, ef_search=16, random_seed=123)
    flat = BruteForceFlatIndex(metric="cosine")

    # Generate 50 synthetic vectors
    for i in range(50):
        v = [rng.uniform(-1.0, 1.0) for _ in range(dim)]
        hnsw.insert(f"doc_{i}", v, metadata={"num": i})
        flat.insert(f"doc_{i}", v, metadata={"num": i})

    query_v = [rng.uniform(-1.0, 1.0) for _ in range(dim)]
    k = 5

    hnsw_res = hnsw.search(query_v, top_k=k)
    flat_res = flat.search(query_v, top_k=k)

    assert len(hnsw_res) == k
    assert len(flat_res) == k

    hnsw_ids = {r[0] for r in hnsw_res}
    flat_ids = {r[0] for r in flat_res}

    overlap = hnsw_ids.intersection(flat_ids)
    recall = len(overlap) / float(k)
    # HNSW should achieve high recall (>= 60% on small random sets, typically >= 80%)
    assert recall >= 0.6


def test_hybrid_metadata_filtering() -> None:
    dim = 4
    hnsw = HNSWIndex(dim=dim, metric="cosine", M=4, random_seed=7)

    hnsw.insert("doc_a", [1.0, 0.0, 0.0, 0.0], metadata={"category": "tech", "tier": "gold"})
    hnsw.insert("doc_b", [0.9, 0.1, 0.0, 0.0], metadata={"category": "sports", "tier": "gold"})
    hnsw.insert("doc_c", [0.8, 0.2, 0.0, 0.0], metadata={"category": "tech", "tier": "silver"})

    query = [1.0, 0.0, 0.0, 0.0]

    # Filter for tech gold only
    res = hnsw.search(
        query,
        top_k=2,
        filter_predicate=lambda m: m.get("category") == "tech" and m.get("tier") == "gold",
    )

    assert len(res) == 1
    assert res[0][0] == "doc_a"
    assert res[0][2]["category"] == "tech"
