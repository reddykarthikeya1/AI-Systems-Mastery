"""Module 20 Test Suite: AI Vector Databases, Cosine Distance & HNSW."""

from __future__ import annotations

import pytest
from vector_engine import FlatVectorIndex, HNSWIndex, VectorItem, VectorMetrics


def test_vector_distance_metrics() -> None:
    # Parallel vectors -> Cosine distance = 0.0
    u = [1.0, 2.0, 3.0]
    v = [2.0, 4.0, 6.0]
    assert pytest.approx(VectorMetrics.cosine_distance(u, v), abs=1e-5) == 0.0

    # Orthogonal vectors -> Cosine distance = 1.0
    a = [1.0, 0.0]
    b = [0.0, 1.0]
    assert pytest.approx(VectorMetrics.cosine_distance(a, b), abs=1e-5) == 1.0

    # Opposite vectors -> Cosine distance = 2.0
    c = [1.0, 0.0]
    d = [-1.0, 0.0]
    assert pytest.approx(VectorMetrics.cosine_distance(c, d), abs=1e-5) == 2.0

    # Euclidean distance
    assert pytest.approx(VectorMetrics.euclidean_distance([0.0, 0.0], [3.0, 4.0]), abs=1e-5) == 5.0


def test_flat_vector_index_exact_knn() -> None:
    index = FlatVectorIndex()
    index.add(VectorItem("doc_a", [1.0, 0.0, 0.0], {"topic": "ai"}))
    index.add(VectorItem("doc_b", [0.0, 1.0, 0.0], {"topic": "web"}))
    index.add(VectorItem("doc_c", [0.9, 0.1, 0.0], {"topic": "ai"}))

    query = [1.0, 0.05, 0.0]
    results = index.search(query, top_k=2)

    assert len(results) == 2
    # doc_a is closest to [1.0, 0.05, 0.0], followed by doc_c
    assert results[0][0].item_id == "doc_a"
    assert results[1][0].item_id == "doc_c"


def test_hnsw_approximate_search() -> None:
    hnsw = HNSWIndex(m=4, ef_construction=16, ef_search=8, max_layers=3)

    # Insert 15 items in 3-dimensional space
    for i in range(15):
        vec = [float(i) / 10.0, 1.0 - float(i) / 10.0, 0.5]
        hnsw.add(VectorItem(f"item_{i}", vec, {"idx": i}))

    query = [0.2, 0.8, 0.5]  # Very close to item_2
    results = hnsw.search(query, top_k=3)

    assert len(results) >= 1
    top_id = results[0][0].item_id
    # Must retrieve item_2 or closely adjacent neighbor item_1 / item_3
    assert top_id in ["item_1", "item_2", "item_3"]


def test_hnsw_metadata_payload_filtering() -> None:
    hnsw = HNSWIndex(m=4, ef_construction=16, ef_search=16, max_layers=3)

    # Laptops (close to [0.9, 0.9, 0.1])
    hnsw.add(VectorItem("laptop_1", [0.95, 0.90, 0.10], {"category": "electronics"}))
    hnsw.add(VectorItem("laptop_2", [0.92, 0.88, 0.12], {"category": "electronics"}))

    # Shoes (further from query)
    hnsw.add(VectorItem("shoe_1", [0.10, 0.20, 0.90], {"category": "footwear"}))
    hnsw.add(VectorItem("shoe_2", [0.12, 0.25, 0.85], {"category": "footwear"}))

    # Query with laptop vector BUT filter by category == "footwear"
    query_laptop = [0.95, 0.90, 0.10]
    results = hnsw.search(query_laptop, top_k=2, filter_payload={"category": "footwear"})

    assert len(results) == 2
    # Even though laptops are closer in vector space, filter strictly ensures only footwear is returned!
    for item, _ in results:
        assert item.payload["category"] == "footwear"


def test_hnsw_vs_flat_recall_evaluation() -> None:
    flat = FlatVectorIndex()
    hnsw = HNSWIndex(m=6, ef_construction=32, ef_search=16, max_layers=3)

    # 20 distinct vectors
    for i in range(20):
        v = [float(i % 5), float((i * 2) % 7), float((i * 3) % 11)]
        item = VectorItem(f"v_{i}", v)
        flat.add(item)
        hnsw.add(item)

    query = [2.5, 4.0, 5.5]

    ground_truth = [item.item_id for item, _ in flat.search(query, top_k=3)]
    ann_results = [item.item_id for item, _ in hnsw.search(query, top_k=3)]

    # Compute intersection recall
    overlap = len(set(ground_truth).intersection(set(ann_results)))
    recall = overlap / len(ground_truth)

    # In small networks HNSW should capture at least 66% to 100% of top-3
    assert recall >= 0.66
