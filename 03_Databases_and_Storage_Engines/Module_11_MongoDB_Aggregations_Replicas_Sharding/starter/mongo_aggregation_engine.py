"""Module 11 Starter: MongoDB Aggregation Pipeline & Sharding Engine.

TODO for Student:
Implement:
1. Multi-stage Aggregation Pipeline ($match, $project, $unwind, $group, $sort, $limit).
2. Distributed Shard Router with Hashed vs Range Partitioning.
3. Targeted routing evaluation vs Cluster-wide Scatter-Gather broadcast.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class AggregationPipeline:
    """Executes sequential MongoDB aggregation stages on an in-memory document stream."""

    def __init__(self, documents: list[dict[str, Any]]) -> None:
        self.stream = [dict(d) for d in documents]

    def match(self, criteria: dict[str, Any]) -> AggregationPipeline:
        """Filters documents matching criteria."""
        raise NotImplementedError("Implement $match stage")

    def unwind(self, array_field: str) -> AggregationPipeline:
        """Deconstructs array field into individual documents."""
        raise NotImplementedError("Implement $unwind stage")

    def group(self, group_by_field: str, accumulators: dict[str, tuple[str, str]]) -> AggregationPipeline:
        """Groups documents and applies accumulators (e.g. {'total': ('$sum', 'price')})."""
        raise NotImplementedError("Implement $group stage")

    def sort(self, sort_field: str, descending: bool = False) -> AggregationPipeline:
        """Sorts documents by field."""
        raise NotImplementedError("Implement $sort stage")

    def execute(self) -> list[dict[str, Any]]:
        return self.stream


@dataclass
class Shard:
    shard_id: str
    documents: dict[str, dict[str, Any]]


class ShardRouter:
    """Simulates mongos query router directing queries to shards."""

    def __init__(self, num_shards: int = 3) -> None:
        self.num_shards = num_shards
        self.shards: list[Shard] = [Shard(f"shard_{i}", {}) for i in range(num_shards)]

    def get_shard_id(self, shard_key_val: str) -> int:
        """Computes hash of shard key to locate target shard."""
        raise NotImplementedError("Implement hashed shard key distribution")

    def insert(self, shard_key_val: str, document: dict[str, Any]) -> str:
        """Routes insert directly to the target shard."""
        raise NotImplementedError("Implement targeted insert")

    def query(self, filter_criteria: dict[str, Any]) -> tuple[list[dict[str, Any]], bool]:
        """Executes query. Returns (results, was_targeted_query)."""
        raise NotImplementedError("Implement query execution with targeted vs scatter-gather detection")
