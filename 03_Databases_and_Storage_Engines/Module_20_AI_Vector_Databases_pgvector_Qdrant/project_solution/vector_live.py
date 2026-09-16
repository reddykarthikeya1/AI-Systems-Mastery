"""Module 20: Real Vector DBs - In-Memory Qdrant & pgvector Operations (Track B).

Interacts directly with Qdrant via official qdrant-client to demonstrate:
1. In-memory / production vector collection lifecycle with distance metrics (Cosine, Dot, Euclid).
2. Dense embedding insertion with structured payload filtering.
3. Approximate Nearest Neighbor (ANN) search with boolean payload filters.
4. Top-K ranking accuracy and score evaluation.
5. In-process execution via QdrantClient(':memory:') providing immediate testability.
"""

from __future__ import annotations

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
