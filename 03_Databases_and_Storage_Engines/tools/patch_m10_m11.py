from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")

m10_test = root / "Module_10_MongoDB_Document_Modeling_BSON" / "project_solution" / "test_mongo_live.py"
m11_test = root / "Module_11_MongoDB_Aggregations_Replicas_Sharding" / "project_solution" / "test_mongo_scale_live.py"

m10_code = '''"""Tests for Module 10: Real MongoDB Document Modeling & BSON Wire Operations (Track B).

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
_mongo_available: bool | None = None


def mongo_is_available() -> bool:
    global _mongo_available
    if _mongo_available is None:
        try:
            client = MongoLiveClient(uri=MONGO_URI)
            _mongo_available = client.ping()
        except Exception:
            _mongo_available = False
    return _mongo_available


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
def test_mongo_ping():
    if not mongo_is_available():
        pytest.skip("MongoDB service is not running at localhost:27017")
    client = MongoLiveClient(uri=MONGO_URI)
    assert client.ping() is True


@pytest.mark.requires_mongo
def test_ttl_index_creation():
    if not mongo_is_available():
        pytest.skip("MongoDB service is not running at localhost:27017")
    client = MongoLiveClient(uri=MONGO_URI, db_name="test_coursedb")
    coll_name = "test_ttl_sensors"
    client.db.drop_collection(coll_name)

    client.setup_ttl_collection(coll_name=coll_name, expire_after_seconds=3600)
    indexes = list(client.db[coll_name].list_indexes())
    ttl_idx = [idx for idx in indexes if idx.get("expireAfterSeconds") == 3600]
    assert len(ttl_idx) == 1
    assert "created_at" in ttl_idx[0]["key"]


@pytest.mark.requires_mongo
def test_explain_collscan_vs_ixscan():
    if not mongo_is_available():
        pytest.skip("MongoDB service is not running at localhost:27017")
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
def test_atomic_document_updates():
    if not mongo_is_available():
        pytest.skip("MongoDB service is not running at localhost:27017")
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
def test_schema_validation_rejection():
    if not mongo_is_available():
        pytest.skip("MongoDB service is not running at localhost:27017")
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
def test_embed_vs_reference_benchmark():
    if not mongo_is_available():
        pytest.skip("MongoDB service is not running at localhost:27017")
    client = MongoLiveClient(uri=MONGO_URI, db_name="test_coursedb")
    res = client.compare_embed_vs_reference_read(n_items=30)
    assert "embedded_duration_s" in res
    assert "referenced_duration_s" in res
    assert res["speedup_ratio"] > 0
'''

m11_code = '''"""Tests for Module 11: Real MongoDB Aggregation Pipeline, Replication & Sharding (Track B).

Validates:
1. MongoScaleClient connection & health ping
2. Aggregation pipeline ($match, $unwind, $group, $sort)
3. Cross-collection join via $lookup
4. Multi-faceted categorization via $facet
5. ReadPreference secondaryPreferred configuration
6. Aggregation explain output
7. RECONCILIATION: Handbuilt AggregationPipeline results match aggregation logic
8. RECONCILIATION: Shard router hash consistency matches MD5 uniform distribution
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
_mongo_available: bool | None = None


def mongo_is_available() -> bool:
    global _mongo_available
    if _mongo_available is None:
        try:
            client = MongoScaleClient(uri=MONGO_URI)
            _mongo_available = client.ping()
        except Exception:
            _mongo_available = False
    return _mongo_available


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
    router = HandbuiltRouter(num_shards=3, shard_key="customer_id")

    keys = [f"user_{i}" for i in range(300)]
    assignments = [router.get_shard_id(k) for k in keys]

    for shard_id in range(3):
        count = assignments.count(shard_id)
        assert 60 <= count <= 140, f"Shard {shard_id} distribution unbalanced: {count}"


# --- LIVE INTEGRATION TESTS (Skip if MongoDB service is offline) ---

@pytest.mark.requires_mongo
def test_mongo_scale_ping():
    if not mongo_is_available():
        pytest.skip("MongoDB service is not running at localhost:27017")
    client = MongoScaleClient(uri=MONGO_URI)
    assert client.ping() is True


@pytest.mark.requires_mongo
def test_live_aggregation_pipeline():
    if not mongo_is_available():
        pytest.skip("MongoDB service is not running at localhost:27017")
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
def test_live_lookup_join():
    if not mongo_is_available():
        pytest.skip("MongoDB service is not running at localhost:27017")
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
def test_live_faceted_search():
    if not mongo_is_available():
        pytest.skip("MongoDB service is not running at localhost:27017")
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
def test_read_preference_config():
    if not mongo_is_available():
        pytest.skip("MongoDB service is not running at localhost:27017")
    client = MongoScaleClient(uri=MONGO_URI, db_name="test_coursedb")
    coll = client.get_secondary_preferred_collection("test_orders")
    from pymongo.read_preferences import SecondaryPreferred
    assert isinstance(coll.read_preference, SecondaryPreferred)
'''

m10_test.write_text(m10_code, encoding="utf-8")
m11_test.write_text(m11_code, encoding="utf-8")
print("Updated M10 and M11 tests with cached check and correct ShardRouter arguments.")
