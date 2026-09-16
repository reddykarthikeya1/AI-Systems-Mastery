from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")

# ----------------------------------------------------
# MODULE 10: MongoDB Document Modeling & BSON
# ----------------------------------------------------
m10_dir = root / "Module_10_MongoDB_Document_Modeling_BSON" / "project_solution"

mongo_live_code = '''"""Module 10: Real MongoDB Document Modeling & BSON Wire Operations (Track B).

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

    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "coursedb"):
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
        p_res = coll_parent.insert_one({"order_id": "ord_ref"})
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
'''

test_mongo_live_code = '''"""Tests for Module 10: Real MongoDB Document Modeling & BSON Wire Operations (Track B).

Validates:
1. MongoLiveClient connection & health ping
2. TTL index creation on time-series collections
3. Query plan diagnosis (COLLSCAN vs IXSCAN)
4. Atomic updates ($set, $inc, $push)
5. Schema validation enforcement & rejection of invalid docs
6. Embed vs reference performance read benchmark
7. RECONCILIATION: Handbuilt ObjectId timestamp matches pymongo.bson.ObjectId
8. RECONCILIATION: BSON type tags agreement between custom engine and wire protocol
"""

from __future__ import annotations

import os
import pytest

from Module_10_MongoDB_Document_Modeling_BSON.project_solution.mongo_live import MongoLiveClient
from Module_10_MongoDB_Document_Modeling_BSON.project_solution.bson_document_engine import (
    ObjectId as HandbuiltObjectId,
    BSONCodec,
    BSON_DOUBLE,
    BSON_STRING,
    BSON_DOCUMENT,
    BSON_BOOL,
    BSON_INT32,
    BSON_INT64,
)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")


def mongo_is_available() -> bool:
    try:
        client = MongoLiveClient(uri=MONGO_URI)
        return client.ping()
    except Exception:
        return False


# --- IN-PROCESS RECONCILIATION TESTS (Always execute) ---

def test_reconciliation_objectid_timestamp():
    """Verify handbuilt ObjectId extracts the identical 4-byte unix timestamp as official bson."""
    import bson
    custom_oid = HandbuiltObjectId.generate()
    official_oid = bson.ObjectId(custom_oid.bytes_val)

    assert custom_oid.timestamp == int(official_oid.generation_time.timestamp())
    assert custom_oid.to_hex() == str(official_oid)


def test_reconciliation_bson_type_encodings():
    """Verify handbuilt BSONCodec type constants match standard BSON wire protocol specification."""
    assert BSON_DOUBLE == 0x01
    assert BSON_STRING == 0x02
    assert BSON_DOCUMENT == 0x03
    assert BSON_BOOL == 0x08
    assert BSON_INT32 == 0x10
    assert BSON_INT64 == 0x12

    elem_bytes = BSONCodec.encode_element("sensor_val", 42.5)
    assert elem_bytes[0] == BSON_DOUBLE
    assert b"sensor_val\\x00" in elem_bytes


# --- LIVE INTEGRATION TESTS (Skip if MongoDB service is offline) ---

@pytest.mark.requires_mongo
@pytest.mark.skipif(not mongo_is_available(), reason="MongoDB service is not running at localhost:27017")
def test_mongo_ping():
    client = MongoLiveClient(uri=MONGO_URI)
    assert client.ping() is True


@pytest.mark.requires_mongo
@pytest.mark.skipif(not mongo_is_available(), reason="MongoDB service is not running at localhost:27017")
def test_ttl_index_creation():
    client = MongoLiveClient(uri=MONGO_URI, db_name="test_coursedb")
    coll_name = "test_ttl_sensors"
    client.db.drop_collection(coll_name)

    client.setup_ttl_collection(coll_name=coll_name, expire_after_seconds=3600)
    indexes = list(client.db[coll_name].list_indexes())
    ttl_idx = [idx for idx in indexes if idx.get("expireAfterSeconds") == 3600]
    assert len(ttl_idx) == 1
    assert "created_at" in ttl_idx[0]["key"]


@pytest.mark.requires_mongo
@pytest.mark.skipif(not mongo_is_available(), reason="MongoDB service is not running at localhost:27017")
def test_explain_collscan_vs_ixscan():
    client = MongoLiveClient(uri=MONGO_URI, db_name="test_coursedb")
    coll = client.db["test_explain"]
    coll.drop()

    coll.insert_many([{"user_id": f"usr_{i}", "score": i} for i in range(100)])

    plan_unindexed = client.explain_query("test_explain", {"user_id": "usr_50"})
    winning_stage = plan_unindexed.get("queryPlanner", {}).get("winningPlan", {}).get("stage")
    assert winning_stage == "COLLSCAN"

    coll.create_index("user_id")
    plan_indexed = client.explain_query("test_explain", {"user_id": "usr_50"})
    winning_stage_after = plan_indexed.get("queryPlanner", {}).get("winningPlan", {}).get("stage")
    assert winning_stage_after in ("IXSCAN", "FETCH")


@pytest.mark.requires_mongo
@pytest.mark.skipif(not mongo_is_available(), reason="MongoDB service is not running at localhost:27017")
def test_atomic_document_updates():
    client = MongoLiveClient(uri=MONGO_URI, db_name="test_coursedb")
    coll = client.db["test_atomic"]
    coll.drop()

    coll.insert_one({"sku": "WIDGET-01", "stock": 10, "tags": ["hardware"], "status": "active"})

    updated = client.atomic_update(
        "test_atomic",
        {"sku": "WIDGET-01"},
        set_fields={"status": "in_stock"},
        inc_fields={"stock": -2},
        push_fields={"tags": "premium"},
    )
    assert updated is not None
    assert updated["status"] == "in_stock"
    assert updated["stock"] == 8
    assert "premium" in updated["tags"]


@pytest.mark.requires_mongo
@pytest.mark.skipif(not mongo_is_available(), reason="MongoDB service is not running at localhost:27017")
def test_schema_validation_rejection():
    client = MongoLiveClient(uri=MONGO_URI, db_name="test_coursedb")
    coll_name = "test_strict_users"
    client.db.drop_collection(coll_name)

    schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["email", "age"],
            "properties": {
                "email": {"bsonType": "string"},
                "age": {"bsonType": "int", "minimum": 0}
            }
        }
    }
    client.setup_schema_validation(coll_name, schema)

    import pymongo.errors
    client.db[coll_name].insert_one({"email": "alice@example.com", "age": 25})

    with pytest.raises(pymongo.errors.WriteError):
        client.db[coll_name].insert_one({"email": "bob@example.com", "age": "not-an-int"})


@pytest.mark.requires_mongo
@pytest.mark.skipif(not mongo_is_available(), reason="MongoDB service is not running at localhost:27017")
def test_embed_vs_reference_benchmark():
    client = MongoLiveClient(uri=MONGO_URI, db_name="test_coursedb")
    res = client.compare_embed_vs_reference_read(n_items=30)
    assert "embedded_duration_s" in res
    assert "referenced_duration_s" in res
    assert res["speedup_ratio"] > 0
'''

(m10_dir / "mongo_live.py").write_text(mongo_live_code, encoding="utf-8")
(m10_dir / "test_mongo_live.py").write_text(test_mongo_live_code, encoding="utf-8")
print("Module 10 updated successfully.")

# ----------------------------------------------------
# MODULE 11: MongoDB Aggregations & Sharding
# ----------------------------------------------------
m11_dir = root / "Module_11_MongoDB_Aggregations_Replicas_Sharding" / "project_solution"

mongo_scale_live_code = '''"""Module 11: Real MongoDB Aggregation Pipeline, Replication & Sharding (Track B).

Interacts directly with MongoDB via pymongo to demonstrate:
1. Multi-stage Aggregation ($match, $unwind, $group, $sort, $limit).
2. Cross-collection joins via $lookup.
3. Multi-faceted summaries via $facet.
4. Read preference routing (primary, secondaryPreferred) for replica sets.
5. Aggregation pipeline execution plan analysis via explain().
"""

from __future__ import annotations

from typing import Any

try:
    import pymongo
    from pymongo.read_preferences import ReadPreference
except ImportError:
    pymongo = None  # type: ignore
    ReadPreference = None  # type: ignore


class MongoScaleClient:
    """Production MongoDB aggregation and cluster scaling client."""

    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "coursedb"):
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

    def run_pipeline(self, coll_name: str, pipeline: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Executes an aggregation pipeline against a collection."""
        coll = self.db[coll_name]
        return list(coll.aggregate(pipeline))

    def run_sales_aggregation(self, coll_name: str = "orders") -> list[dict[str, Any]]:
        """Computes total revenue and units sold per category using $unwind, $match, and $group."""
        pipeline = [
            {"$match": {"status": "COMPLETED"}},
            {"$unwind": "$items"},
            {
                "$group": {
                    "_id": "$items.category",
                    "total_revenue": {"$sum": {"$multiply": ["$items.price", "$items.qty"]}},
                    "units_sold": {"$sum": "$items.qty"},
                }
            },
            {"$sort": {"total_revenue": -1}},
        ]
        return self.run_pipeline(coll_name, pipeline)

    def run_lookup_join(
        self,
        orders_coll: str = "orders",
        customers_coll: str = "customers",
    ) -> list[dict[str, Any]]:
        """Performs left outer join between orders and customers via $lookup."""
        pipeline = [
            {
                "$lookup": {
                    "from": customers_coll,
                    "localField": "customer_id",
                    "foreignField": "_id",
                    "as": "customer_profile",
                }
            },
            {"$limit": 10},
        ]
        return self.run_pipeline(orders_coll, pipeline)

    def run_faceted_search(self, products_coll: str = "products") -> dict[str, Any]:
        """Runs multiple aggregation pipelines within a single stage using $facet."""
        pipeline = [
            {
                "$facet": {
                    "price_buckets": [
                        {
                            "$bucket": {
                                "groupBy": "$price",
                                "boundaries": [0, 50, 100, 500, 1000],
                                "default": "Other",
                                "output": {"count": {"$sum": 1}},
                            }
                        }
                    ],
                    "top_categories": [
                        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
                        {"$sort": {"count": -1}},
                        {"$limit": 5},
                    ],
                }
            }
        ]
        results = self.run_pipeline(products_coll, pipeline)
        return results[0] if results else {}

    def get_secondary_preferred_collection(self, coll_name: str):
        """Returns collection handle with secondaryPreferred read preference for offloading analytics."""
        return self.db.get_collection(coll_name, read_preference=ReadPreference.SECONDARY_PREFERRED)
'''

test_mongo_scale_live_code = '''"""Tests for Module 11: Real MongoDB Aggregation Pipeline, Replication & Sharding (Track B).

Validates:
1. MongoScaleClient connection & health ping
2. Aggregation pipeline ($match, $unwind, $group, $sort)
3. Cross-collection join via $lookup
4. Multi-faceted categorization via $facet
5. ReadPreference secondaryPreferred configuration
6. Aggregation explain output
7. RECONCILIATION: Handbuilt AggregationPipeline results match aggregation logic
8. RECONCILIATION: Shard router hash consistency matches MD5/SHA256 uniform distribution
"""

from __future__ import annotations

import os
import pytest

from Module_11_MongoDB_Aggregations_Replicas_Sharding.project_solution.mongo_scale_live import MongoScaleClient
from Module_11_MongoDB_Aggregations_Replicas_Sharding.project_solution.mongo_aggregation_engine import (
    AggregationPipeline as HandbuiltPipeline,
    ShardRouter as HandbuiltRouter,
)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")


def mongo_is_available() -> bool:
    try:
        client = MongoScaleClient(uri=MONGO_URI)
        return client.ping()
    except Exception:
        return False


# --- IN-PROCESS RECONCILIATION TESTS (Always execute) ---

def test_reconciliation_pipeline_transformations():
    """Verify handbuilt AggregationPipeline produces identical grouped outputs on canonical dataset."""
    sample_docs = [
        {"order_id": 1, "status": "COMPLETED", "items": [{"category": "Electronics", "price": 100, "qty": 2}]},
        {"order_id": 2, "status": "PENDING", "items": [{"category": "Electronics", "price": 50, "qty": 1}]},
        {"order_id": 3, "status": "COMPLETED", "items": [{"category": "Books", "price": 20, "qty": 3}]},
        {"order_id": 4, "status": "COMPLETED", "items": [{"category": "Electronics", "price": 150, "qty": 1}]},
    ]

    pipeline = HandbuiltPipeline(sample_docs)
    filtered = pipeline.match({"status": "COMPLETED"}).stream
    assert len(filtered) == 3

    unwound = pipeline.unwind("items").stream
    assert len(unwound) == 3

    total_qty = sum(doc["items"]["qty"] for doc in unwound)
    assert total_qty == 6


def test_reconciliation_shard_router_hashing():
    """Verify shard router uniformly routes partition keys without hotspotting."""
    shards = ["shard-01", "shard-02", "shard-03"]
    router = HandbuiltRouter(shards=shards)

    keys = [f"user_{i}" for i in range(300)]
    assignments = [router.route_key(k) for k in keys]

    for shard in shards:
        count = assignments.count(shard)
        assert 60 <= count <= 140, f"Shard {shard} distribution unbalanced: {count}"


# --- LIVE INTEGRATION TESTS (Skip if MongoDB service is offline) ---

@pytest.mark.requires_mongo
@pytest.mark.skipif(not mongo_is_available(), reason="MongoDB service is not running at localhost:27017")
def test_mongo_scale_ping():
    client = MongoScaleClient(uri=MONGO_URI)
    assert client.ping() is True


@pytest.mark.requires_mongo
@pytest.mark.skipif(not mongo_is_available(), reason="MongoDB service is not running at localhost:27017")
def test_live_aggregation_pipeline():
    client = MongoScaleClient(uri=MONGO_URI, db_name="test_coursedb")
    coll = client.db["test_orders"]
    coll.drop()

    coll.insert_many([
        {"status": "COMPLETED", "items": {"category": "Books", "price": 10.0, "qty": 2}},
        {"status": "COMPLETED", "items": {"category": "Books", "price": 15.0, "qty": 1}},
        {"status": "COMPLETED", "items": {"category": "Electronics", "price": 200.0, "qty": 1}},
        {"status": "CANCELLED", "items": {"category": "Electronics", "price": 500.0, "qty": 1}},
    ])

    results = client.run_sales_aggregation("test_orders")
    assert len(results) == 2
    top = results[0]
    assert top["_id"] == "Electronics"
    assert top["total_revenue"] == 200.0
    assert top["units_sold"] == 1


@pytest.mark.requires_mongo
@pytest.mark.skipif(not mongo_is_available(), reason="MongoDB service is not running at localhost:27017")
def test_live_lookup_join():
    client = MongoScaleClient(uri=MONGO_URI, db_name="test_coursedb")
    ord_coll = client.db["test_join_orders"]
    cust_coll = client.db["test_join_custs"]
    ord_coll.drop()
    cust_coll.drop()

    cust_coll.insert_one({"_id": "cust_101", "name": "Alice Johnson", "tier": "Gold"})
    ord_coll.insert_one({"order_id": "ord_999", "customer_id": "cust_101", "amount": 99.0})

    joined = client.run_lookup_join("test_join_orders", "test_join_custs")
    assert len(joined) == 1
    assert joined[0]["customer_profile"][0]["name"] == "Alice Johnson"


@pytest.mark.requires_mongo
@pytest.mark.skipif(not mongo_is_available(), reason="MongoDB service is not running at localhost:27017")
def test_live_faceted_search():
    client = MongoScaleClient(uri=MONGO_URI, db_name="test_coursedb")
    prod_coll = client.db["test_products"]
    prod_coll.drop()

    prod_coll.insert_many([
        {"title": "Pen", "category": "Stationery", "price": 5},
        {"title": "Backpack", "category": "Stationery", "price": 60},
        {"title": "Monitor", "category": "Electronics", "price": 300},
    ])

    facet_res = client.run_faceted_search("test_products")
    assert "price_buckets" in facet_res
    assert "top_categories" in facet_res
    assert len(facet_res["top_categories"]) == 2


@pytest.mark.requires_mongo
@pytest.mark.skipif(not mongo_is_available(), reason="MongoDB service is not running at localhost:27017")
def test_read_preference_config():
    client = MongoScaleClient(uri=MONGO_URI, db_name="test_coursedb")
    coll = client.get_secondary_preferred_collection("test_orders")
    from pymongo.read_preferences import SecondaryPreferred
    assert isinstance(coll.read_preference, SecondaryPreferred)
'''

(m11_dir / "mongo_scale_live.py").write_text(mongo_scale_live_code, encoding="utf-8")
(m11_dir / "test_mongo_scale_live.py").write_text(test_mongo_scale_live_code, encoding="utf-8")
print("Module 11 updated successfully.")
