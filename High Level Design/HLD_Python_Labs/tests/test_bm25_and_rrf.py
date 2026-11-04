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


def test_bm25_reindexing_and_postings_consistency_regression():
    """EXACT REGRESSION TEST:

    Re-index doc_id 1 with completely new text and verify:
    1. Old tokens are completely purged from postings and inverted index.
    2. Document frequency n(q) of old terms decrements or removes empty keys.
    3. Document length and total_tokens are exactly updated without inflation.
    4. Searching for old words returns 0 results for doc1.
    """
    index = BM25Index(k1=1.5, b=0.75)
    index.add_document("doc1", "quantum physics entanglement qubits")
    index.add_document("doc2", "classical physics thermodynamics")

    assert index.total_docs == 2
    assert "qubits" in index.inverted_index
    assert "doc1" in index.inverted_index["qubits"]
    assert index.doc_lengths["doc1"] == 4
    initial_total_tokens = index.total_tokens

    # Re-index doc1 with completely different topic
    index.add_document("doc1", "relational database indexing btree")

    # Document count must still be 2, not 3
    assert index.total_docs == 2
    assert index.doc_lengths["doc1"] == 4
    # Total tokens must match actual sum of current docs
    assert index.total_tokens == len("relational database indexing btree".split()) + len("classical physics thermodynamics".split())

    # CRITICAL: Old terms ("qubits", "entanglement") must NO LONGER point to doc1!
    assert "qubits" not in index.inverted_index
    assert "entanglement" not in index.inverted_index
    assert "doc1" not in index.inverted_index.get("physics", {})

    # New terms must exist
    assert "doc1" in index.inverted_index["btree"]

    # Search for old words must NOT find doc1
    results_old = index.search("qubits entanglement", top_k=5)
    assert not any(r.doc_id == "doc1" for r in results_old)

    # Search for new words must find doc1
    results_new = index.search("btree database", top_k=5)
    assert any(r.doc_id == "doc1" for r in results_new)


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


def test_bm25_parameter_validation():
    with pytest.raises(ValueError):
        BM25Index(k1=-0.5)
    with pytest.raises(ValueError):
        BM25Index(b=1.5)
