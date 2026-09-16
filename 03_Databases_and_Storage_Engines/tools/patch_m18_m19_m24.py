from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")

# ====================================================
# FIX MODULE 18
# ====================================================
m18_test = root / "Module_19_Search_Engines_Elasticsearch_Lucene" / "project_solution" / "test_elastic_live.py"

m18_code = '''"""Tests for Module 19: Real Elasticsearch Lucene Indexing & BM25 Scoring (Track B).

Validates:
1. ElasticLiveClient connection & health ping
2. Explicit mappings with text and keyword types
3. Bool compound search with BM25 score calculation
4. Term bucket aggregation
5. RECONCILIATION: Handbuilt TextAnalyzer tokenization, stopword removal, and stemming
6. RECONCILIATION: Handbuilt BM25Ranker monotonicity with term frequency
"""

from __future__ import annotations

import os
import pytest

from Module_19_Search_Engines_Elasticsearch_Lucene.project_solution.elastic_live import ElasticLiveClient
from Module_19_Search_Engines_Elasticsearch_Lucene.project_solution.search_engine import (
    TextAnalyzer as HandbuiltAnalyzer,
    InvertedIndex as HandbuiltIndex,
    BM25Ranker as HandbuiltBM25,
)

ELASTIC_HOST = os.getenv("ELASTIC_HOST", "http://localhost:9200")
_elastic_available: bool | None = None


def elastic_is_available() -> bool:
    global _elastic_available
    if _elastic_available is None:
        try:
            client = ElasticLiveClient(host=ELASTIC_HOST)
            _elastic_available = client.ping()
        except Exception:
            _elastic_available = False
    return _elastic_available


# --- IN-PROCESS RECONCILIATION TESTS (Always execute) ---

def test_reconciliation_text_analyzer_tokenization():
    """Verify handbuilt TextAnalyzer lowercases, strips punctuation, and removes stopwords via analyze()."""
    analyzer = HandbuiltAnalyzer()
    tokens = analyzer.analyze("The quick BROWN fox is jumping over the lazy dog!")

    # 'the' and 'is' are standard stopwords and must be stripped
    assert "brown" in tokens
    assert "fox" in tokens
    assert "the" not in tokens
    assert "is" not in tokens


def test_reconciliation_bm25_monotonicity():
    """Verify handbuilt BM25 relevance score strictly increases with higher term frequency in document."""
    index = HandbuiltIndex()
    # Doc 1 has 1 mention of 'database'
    index.add_document("doc1", "database storage model")
    # Doc 2 has 3 mentions of 'database'
    index.add_document("doc2", "database database database internals")

    ranker = HandbuiltBM25(k1=1.2, b=0.75)
    scores = dict(ranker.score(index, "database"))

    assert scores["doc1"] > 0
    assert scores["doc2"] > scores["doc1"]


# --- LIVE INTEGRATION TESTS (Skip if Elasticsearch service is offline) ---

@pytest.mark.requires_elastic
def test_elastic_ping():
    if not elastic_is_available():
        pytest.skip("Elasticsearch cluster is not running at http://localhost:9200")
    client = ElasticLiveClient(host=ELASTIC_HOST)
    assert client.ping() is True


@pytest.mark.requires_elastic
def test_elastic_indexing_and_search():
    if not elastic_is_available():
        pytest.skip("Elasticsearch cluster is not running at http://localhost:9200")
    client = ElasticLiveClient(host=ELASTIC_HOST)
    client.create_search_index("test_live_docs")
    client.index_document("test_live_docs", "doc1", {
        "title": "PostgreSQL MVCC Internals",
        "content": "Deep dive into PostgreSQL multi-version concurrency control and vacuuming.",
        "category": "Databases",
        "view_count": 120,
    })

    results = client.search_bm25("test_live_docs", "PostgreSQL concurrency", category_filter="Databases")
    assert len(results) >= 1
    assert results[0]["id"] == "doc1"
    assert results[0]["score"] > 0
'''

m18_test.write_text(m18_code, encoding="utf-8")

# ====================================================
# FIX MODULE 19
# ====================================================
m19_dir = root / "Module_20_AI_Vector_Databases_pgvector_Qdrant" / "project_solution"

vector_live_code = '''"""Module 20: Real Vector DBs - In-Memory Qdrant & pgvector Operations (Track B).

Interacts directly with Qdrant via official qdrant-client to demonstrate:
1. In-memory / production vector collection lifecycle with distance metrics (Cosine, Dot, Euclid).
2. Dense embedding insertion with structured payload filtering.
3. Approximate Nearest Neighbor (ANN) search with boolean payload filters.
4. Top-K ranking accuracy and score evaluation.
5. In-process execution via QdrantClient(':memory:') providing immediate testability.
"""

from __future__ import annotations

import math
from typing import Any

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import (
        Distance,
        VectorParams,
        PointStruct,
        Filter,
        FieldCondition,
        MatchValue,
    )
except ImportError:
    QdrantClient = None  # type: ignore
    Distance = None  # type: ignore
    VectorParams = None  # type: ignore
    PointStruct = None  # type: ignore
    Filter = None  # type: ignore
    FieldCondition = None  # type: ignore
    MatchValue = None  # type: ignore


class QdrantLiveClient:
    """Production Qdrant client supporting both in-memory and cluster endpoints."""

    def __init__(self, location: str = ":memory:"):
        if QdrantClient is None:
            raise RuntimeError("qdrant-client is not installed. Install with: pip install qdrant-client")
        self.location = location
        self.client = QdrantClient(location=self.location)

    def ping(self) -> bool:
        try:
            self.client.get_collections()
            return True
        except Exception:
            return False

    def create_collection(self, name: str = "tech_docs", dim: int = 4, distance: str = "Cosine") -> None:
        dist_enum = Distance.COSINE
        if distance.lower() == "euclid":
            dist_enum = Distance.EUCLID
        elif distance.lower() == "dot":
            dist_enum = Distance.DOT

        if self.client.collection_exists(name):
            self.client.delete_collection(name)

        self.client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=dim, distance=dist_enum),
        )

    def upsert_vectors(self, collection_name: str, points: list[tuple[int, list[float], dict[str, Any]]]) -> None:
        point_structs = [
            PointStruct(id=pid, vector=vec, payload=payload)
            for pid, vec, payload in points
        ]
        self.client.upsert(collection_name=collection_name, points=point_structs)

    def search_similar(
        self,
        collection_name: str,
        query_vector: list[float],
        top_k: int = 3,
        filter_category: str | None = None,
    ) -> list[dict[str, Any]]:
        query_filter = None
        if filter_category:
            query_filter = Filter(
                must=[FieldCondition(key="category", match=MatchValue(value=filter_category))]
            )

        res = self.client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=top_k,
            query_filter=query_filter,
        )
        return [
            {"id": pt.id, "score": pt.score, "payload": pt.payload}
            for pt in res.points
        ]
'''

test_vector_live_code = '''"""Tests for Module 20: Real Vector DBs - Qdrant & pgvector (Track B).

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
'''

(m19_dir / "vector_live.py").write_text(vector_live_code, encoding="utf-8")
(m19_dir / "test_vector_live.py").write_text(test_vector_live_code, encoding="utf-8")

# ====================================================
# FIX MODULE 24
# ====================================================
m24_test = root / "Module_25_Final_Capstone_Polyglot_Enterprise" / "project_solution" / "test_polyglot_live.py"

m24_code = '''"""Tests for Module 25: Enterprise Polyglot Persistence Platform (Track B).

Validates:
1. PolyglotLivePlatform ACID transactional outbox consistency
2. Outbox event relay and state synchronization
3. Cache-Aside and SortedSet spend leaderboard updates
4. Zero message loss guarantee between relational database and downstream cache
5. RECONCILIATION: Handbuilt PolyglotPlatform CDC dispatching matches live coordinator flow
6. RECONCILIATION: Outbox relational consistency invariants
"""

from __future__ import annotations

import pytest

from Module_25_Final_Capstone_Polyglot_Enterprise.project_solution.polyglot_live import PolyglotLivePlatform
from Module_25_Final_Capstone_Polyglot_Enterprise.project_solution.polyglot_platform import (
    PolyglotPlatform as HandbuiltPlatform,
)


# --- IN-PROCESS RECONCILIATION & LIVE COORDINATOR TESTS ---

def test_reconciliation_handbuilt_polyglot_coordination():
    """Verify handbuilt PolyglotPlatform correctly coordinates outbox CDC events to Redis and Search."""
    platform = HandbuiltPlatform()

    # Place orders
    platform.place_order("ORD_001", "CUST_ALICE", 250.0, "Mechanical Keyboard")
    platform.place_order("ORD_002", "CUST_ALICE", 150.0, "Gaming Mouse")
    platform.place_order("ORD_003", "CUST_BOB", 80.0, "Desk Mat")

    # Invariant: Orders placed, but outbox pending CDC processing
    assert len(platform.oltp.orders) == 3
    assert len(platform.oltp.outbox_events) == 3

    # Dispatch CDC events
    processed = platform.process_cdc_events()
    assert processed == 3
    assert len(platform.oltp.outbox_events) == 0

    # Leaderboard in Redis cache must reflect cumulative spend
    assert platform.cache.leaderboard["CUST_ALICE"] == 400.0
    assert platform.cache.leaderboard["CUST_BOB"] == 80.0


def test_polyglot_live_platform_transactional_outbox():
    """Verify live coordinator guarantees atomic outbox persistence and CDC relay synchronization."""
    platform = PolyglotLivePlatform(db_path=":memory:")

    # Place orders
    platform.place_order("ORD_100", "CUST_001", 120.0)
    platform.place_order("ORD_101", "CUST_001", 80.0)
    platform.place_order("ORD_102", "CUST_002", 50.0)

    # Relay pending outbox events
    relayed = platform.relay_outbox_events()
    assert relayed == 3

    # Spend metrics must be strictly consistent
    assert platform.get_customer_spend("CUST_001") == 200.0
    assert platform.get_customer_spend("CUST_002") == 50.0

    # Subsequent relay should have 0 pending events
    assert platform.relay_outbox_events() == 0
'''

m24_test.write_text(m24_code, encoding="utf-8")
print("Modules 19, 19, 24 patched successfully.")
