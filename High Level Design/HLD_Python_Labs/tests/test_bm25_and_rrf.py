"""Tests for BM25 Lexical, Dense Vector Cosine & Reciprocal Rank Fusion (Chapter 21)."""
import pytest
from ch21_distributed_search.bm25_and_rrf import (
    BM25Index,
    DenseVectorIndex,
    HybridSearchEngine,
    reciprocal_rank_fusion,
    SearchResult,
)


def test_bm25_ranking():
    index = BM25Index(k1=1.5, b=0.75)
    index.add_document("doc1", "distributed databases rely on two phase commit or sagas")
    index.add_document("doc2", "chocolate cake recipe with dark cocoa and fresh cream")
    index.add_document("doc3", "high level design of distributed caching and databases")

    results = index.search("distributed databases", top_k=2)
    assert len(results) == 2
    top_doc_ids = [r.doc_id for r in results]
    assert "doc1" in top_doc_ids
    assert "doc3" in top_doc_ids
    assert "doc2" not in top_doc_ids


def test_dense_vector_search():
    index = DenseVectorIndex()
    # 3-dim mock vectors
    index.add_document("vec1", [1.0, 0.0, 0.0], content="Alpha")
    index.add_document("vec2", [0.0, 1.0, 0.0], content="Beta")
    index.add_document("vec3", [0.707, 0.707, 0.0], content="Gamma")

    # Query aligned with [1.0, 0.0, 0.0]
    results = index.search([1.0, 0.0, 0.0], top_k=2)
    assert results[0].doc_id == "vec1"
    assert results[0].score == pytest.approx(1.0)
    assert results[1].doc_id == "vec3"


def test_reciprocal_rank_fusion():
    # Rank list 1 (Lexical)
    list_lexical = [
        SearchResult(doc_id="D1", score=10.0, rank=1),
        SearchResult(doc_id="D2", score=8.0, rank=2),
        SearchResult(doc_id="D3", score=5.0, rank=3),
    ]

    # Rank list 2 (Dense)
    list_dense = [
        SearchResult(doc_id="D2", score=0.95, rank=1),
        SearchResult(doc_id="D1", score=0.80, rank=2),
        SearchResult(doc_id="D4", score=0.70, rank=3),
    ]

    # Cormack RRF with k=60
    fused = reciprocal_rank_fusion([list_lexical, list_dense], k=60, top_k=4)

    # D1 score: 1/(60+1) + 1/(60+2) = 1/61 + 1/62 = 0.01639 + 0.01612 = 0.03251
    # D2 score: 1/(60+2) + 1/(60+1) = 0.03251
    # Both D1 and D2 should occupy top 2 positions
    top_two = {fused[0].doc_id, fused[1].doc_id}
    assert top_two == {"D1", "D2"}


def test_hybrid_search_engine():
    engine = HybridSearchEngine(k_rrf=60)
    engine.add_document("d1", "kafka stream processing", [1.0, 0.0])
    engine.add_document("d2", "postgresql relational storage", [0.0, 1.0])

    results = engine.search_hybrid("kafka", [1.0, 0.0], top_k=1)
    assert len(results) == 1
    assert results[0].doc_id == "d1"
