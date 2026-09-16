"""Module 10: Real MongoDB Document Modeling & BSON Wire Operations (Track B).

Interacts directly with MongoDB via pymongo to demonstrate:
1. Embedding vs Referencing performance trade-offs under 1:N relationships.
2. TTL indexes automatically expiring time-series documents.
3. Query plan diagnosis using explain() verifying COLLSCAN -> IXSCAN transition.
4. Schema validation with JSON Schema validators at the collection level.
5. Atomic document updates with $set, $inc, and $push.
"""

from __future__ import annotations


import time
from datetime import datetime, timezone
from typing import Any

try:
    import pymongo
    from bson import ObjectId as PyMongoObjectId
except ImportError:
    pymongo = None  # type: ignore
    PyMongoObjectId = None  # type: ignore


class MongoLiveClient:
    """Production MongoDB client for document modeling patterns."""

    def __init__(self, uri: str = "mongodb://localhost:17017/?directConnection=true", db_name: str = "coursedb"):
        if pymongo is None:
            raise RuntimeError("pymongo is not installed. Install with: pip install pymongo")
        self.client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=2000)
        self.db = self.client[db_name]

    def ping(self) -> bool:
        try:
            self.client.admin.command("ping")
            return True
        except Exception:
            return False

    def setup_ttl_collection(self, coll_name: str = "sensor_readings", expire_after_seconds: int = 10) -> None:
        coll = self.db[coll_name]
        coll.create_index("created_at", expireAfterSeconds=expire_after_seconds)

    def insert_sensor_data(self, coll_name: str, device_id: str, reading: float) -> str:
        coll = self.db[coll_name]
        res = coll.insert_one({
            "device_id": device_id,
            "reading": reading,
            "created_at": datetime.now(timezone.utc),
        })
        return str(res.inserted_id)

    def explain_query(self, coll_name: str, filter_dict: dict[str, Any]) -> dict[str, Any]:
        coll = self.db[coll_name]
        return coll.find(filter_dict).explain()

    def setup_schema_validation(self, coll_name: str, validator: dict[str, Any]) -> None:
        """Configures JSON schema validator for a collection."""
        if coll_name in self.db.list_collection_names():
            self.db.command("collMod", coll_name, validator=validator, validationLevel="strict")
        else:
            self.db.create_collection(coll_name, validator=validator, validationLevel="strict")

    def atomic_update(
        self,
        coll_name: str,
        filter_dict: dict[str, Any],
        set_fields: dict[str, Any] | None = None,
        inc_fields: dict[str, Any] | None = None,
        push_fields: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Applies $set, $inc, and $push in a single atomic find_one_and_update call."""
        update_doc: dict[str, Any] = {}
        if set_fields:
            update_doc["$set"] = set_fields
        if inc_fields:
            update_doc["$inc"] = inc_fields
        if push_fields:
            update_doc["$push"] = push_fields

        coll = self.db[coll_name]
        return coll.find_one_and_update(
            filter_dict,
            update_doc,
            return_document=pymongo.ReturnDocument.AFTER,
        )

    def compare_embed_vs_reference_read(self, n_items: int = 50) -> dict[str, float]:
        """Compares 1 document read (embedded) vs 1 + N reads (referenced)."""
        coll_embed = self.db["bench_embedded"]
        coll_parent = self.db["bench_parent"]
        coll_children = self.db["bench_children"]

        coll_embed.delete_many({})
        coll_parent.delete_many({})
        coll_children.delete_many({})

        # Insert embedded
        coll_embed.insert_one({
            "order_id": "ord_embed",
            "items": [{"sku": f"SKU_{i}", "qty": 1} for i in range(n_items)]
        })

        # Insert referenced
        parent_result = coll_parent.insert_one({"order_id": "ord_ref"})
        assert parent_result.acknowledged, "write concern did not acknowledge the parent insert"
        coll_children.insert_many([{"order_id": "ord_ref", "sku": f"SKU_{i}"} for i in range(n_items)])

        # Measure embedded read (Single round-trip)
        start_embed = time.perf_counter()
        _ = coll_embed.find_one({"order_id": "ord_embed"})
        embed_time = time.perf_counter() - start_embed

        # Measure referenced read (Two queries / join)
        start_ref = time.perf_counter()
        _ = coll_parent.find_one({"order_id": "ord_ref"})
        _ = list(coll_children.find({"order_id": "ord_ref"}))
        ref_time = time.perf_counter() - start_ref

        return {
            "embedded_duration_s": embed_time,
            "referenced_duration_s": ref_time,
            "speedup_ratio": ref_time / embed_time if embed_time > 0 else 1.0,
        }
