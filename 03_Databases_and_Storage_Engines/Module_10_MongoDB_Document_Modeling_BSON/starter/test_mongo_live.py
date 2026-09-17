"""Tests for Module 10: Real MongoDB Document Modeling & BSON Wire Operations (Track B).

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

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:17017/?directConnection=true")
_mongo_available: bool | None = None


def mongo_is_available() -> bool:
    global _mongo_available
    if _mongo_available is None:
        try:
            client = MongoLiveClient(uri=MONGO_URI)
            if not client.ping():
                _mongo_available = False
            else:
                hello = client.client.admin.command("hello")
                _mongo_available = bool(hello.get("isWritablePrimary", hello.get("ismaster", False)))
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
    assert b"sensor_val\x00" in elem_bytes


# --- LIVE INTEGRATION TESTS (Skip if MongoDB service is offline) ---

@pytest.mark.requires_mongo
def test_mongo_ping():
    if not mongo_is_available():
        pytest.skip("MongoDB service is not running at localhost:17017")
    client = MongoLiveClient(uri=MONGO_URI)
    assert client.ping() is True


@pytest.mark.requires_mongo
def test_ttl_index_creation():
    if not mongo_is_available():
        pytest.skip("MongoDB service is not running at localhost:17017")
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
        pytest.skip("MongoDB service is not running at localhost:17017")
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
        pytest.skip("MongoDB service is not running at localhost:17017")
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
        pytest.skip("MongoDB service is not running at localhost:17017")
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
        pytest.skip("MongoDB service is not running at localhost:17017")
    client = MongoLiveClient(uri=MONGO_URI, db_name="test_coursedb")
    res = client.compare_embed_vs_reference_read(n_items=30)
    assert "embedded_duration_s" in res
    assert "referenced_duration_s" in res
    assert res["speedup_ratio"] > 0
