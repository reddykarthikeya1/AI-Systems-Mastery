"""Module 11: MongoDB Aggregation Pipeline & Sharding Engine Reference Solution.

This is a pure-Python MODEL of MongoDB's aggregation pipeline and sharded cluster routing, built to make the
mechanism visible. It does not connect to MongoDB. For the real driver,
real queries and real operational behaviour, see `mongo_scale_live.py`.

Implements:
1. Multi-stage Aggregation Pipeline ($match, $unwind, $group, $sort, $limit).
2. Distributed Shard Router with Hashed Partitioning.
3. Targeted routing evaluation vs Cluster-wide Scatter-Gather broadcast.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
import hashlib
from typing import Any


class AggregationPipeline:
    """Executes sequential MongoDB aggregation stages on an in-memory document stream."""

    def __init__(self, documents: list[dict[str, Any]]) -> None:
        self.stream = [dict(d) for d in documents]

    def match(self, criteria: dict[str, Any]) -> AggregationPipeline:
        """Filters documents matching criteria ($match)."""
        filtered = []
        for doc in self.stream:
            matches = True
            for k, v in criteria.items():
                if doc.get(k) != v:
                    matches = False
                    break
            if matches:
                filtered.append(doc)
        self.stream = filtered
        return self

    def unwind(self, array_field: str) -> AggregationPipeline:
        """Deconstructs array field into individual documents ($unwind)."""
        unwound = []
        for doc in self.stream:
            items = doc.get(array_field, [])
            if isinstance(items, list):
                for item in items:
                    new_doc = dict(doc)
                    new_doc[array_field] = item
                    unwound.append(new_doc)
            else:
                unwound.append(doc)
        self.stream = unwound
        return self

    def group(self, group_by_field: str, accumulators: dict[str, tuple[str, str]]) -> AggregationPipeline:
        """Groups documents and applies accumulators (e.g. {'total': ('$sum', 'price')})."""
        grouped: dict[Any, list[dict[str, Any]]] = defaultdict(list)
        for doc in self.stream:
            key_val = doc
            for part in group_by_field.split("."):
                if isinstance(key_val, dict):
                    key_val = key_val.get(part)
            grouped[key_val].append(doc)

        result = []
        for key_val, doc_list in grouped.items():
            row: dict[str, Any] = {"_id": key_val}
            for out_col, (op, target_field) in accumulators.items():
                # Extract values from nested or direct fields
                values = []
                for d in doc_list:
                    val = d
                    for part in target_field.split("."):
                        if isinstance(val, dict):
                            val = val.get(part)
                    if isinstance(val, (int, float)):
                        values.append(val)

                if op == "$sum":
                    row[out_col] = sum(values)
                elif op == "$avg":
                    row[out_col] = round(sum(values) / len(values), 2) if values else 0.0
                elif op == "$count":
                    row[out_col] = len(doc_list)
                elif op == "$max":
                    row[out_col] = max(values) if values else 0
                elif op == "$min":
                    row[out_col] = min(values) if values else 0

            result.append(row)

        self.stream = result
        return self

    def sort(self, sort_field: str, descending: bool = False) -> AggregationPipeline:
        """Sorts documents by field ($sort)."""
        self.stream.sort(key=lambda x: x.get(sort_field, 0), reverse=descending)
        return self

    def limit(self, count: int) -> AggregationPipeline:
        """Limits document stream count ($limit)."""
        self.stream = self.stream[:count]
        return self

    def execute(self) -> list[dict[str, Any]]:
        return self.stream


@dataclass
class Shard:
    shard_id: str
    documents: dict[str, dict[str, Any]] = field(default_factory=dict)


class ShardRouter:
    """Simulates mongos query router directing queries to shards."""

    def __init__(self, num_shards: int = 3, shard_key: str = "customer_id") -> None:
        self.num_shards = num_shards
        self.shard_key = shard_key
        self.shards: list[Shard] = [Shard(f"shard_{i}") for i in range(num_shards)]

    def get_shard_id(self, shard_key_val: str) -> int:
        """Computes hash of shard key to locate target shard."""
        h = int(hashlib.md5(str(shard_key_val).encode("utf-8")).hexdigest(), 16)
        return h % self.num_shards

    def insert(self, document: dict[str, Any]) -> str:
        """Routes insert directly to the target shard based on shard key."""
        if self.shard_key not in document:
            raise KeyError(f"Document missing required shard key: '{self.shard_key}'")

        key_val = str(document[self.shard_key])
        shard_idx = self.get_shard_id(key_val)
        doc_id = str(document.get("_id", f"doc_{len(self.shards[shard_idx].documents) + 1}"))
        stored_doc = dict(document)
        stored_doc["_id"] = doc_id

        self.shards[shard_idx].documents[doc_id] = stored_doc
        return doc_id

    def query(self, filter_criteria: dict[str, Any]) -> tuple[list[dict[str, Any]], bool]:
        """Executes query. Returns (results, was_targeted_query)."""
        # Targeted Query fast-path
        if self.shard_key in filter_criteria:
            target_val = str(filter_criteria[self.shard_key])
            shard_idx = self.get_shard_id(target_val)
            matched = []
            for doc in self.shards[shard_idx].documents.values():
                if all(doc.get(k) == v for k, v in filter_criteria.items()):
                    matched.append(dict(doc))
            return matched, True

        # Scatter-Gather Query: Broadcast to ALL shards
        all_matched = []
        for s in self.shards:
            for doc in s.documents.values():
                if all(doc.get(k) == v for k, v in filter_criteria.items()):
                    all_matched.append(dict(doc))
        return all_matched, False
