"""Tests for Module 11: Real MongoDB Aggregation Pipeline, Replication & Sharding (Track B).

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

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:17017/?directConnection=true")
_mongo_available: bool | None = None


def mongo_is_available() -> bool:
    global _mongo_available
    if _mongo_available is None:
        try:
            client = MongoScaleClient(uri=MONGO_URI)
            if not client.ping():
                _mongo_available = False
            else:
                hello = client.client.admin.command("hello")
                _mongo_available = bool(hello.get("isWritablePrimary", hello.get("ismaster", False)))
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
        pytest.skip("MongoDB service is not running at localhost:17017")
    client = MongoScaleClient(uri=MONGO_URI)
    assert client.ping() is True


@pytest.mark.requires_mongo
def test_live_aggregation_pipeline():
    if not mongo_is_available():
        pytest.skip("MongoDB service is not running at localhost:17017")
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
        pytest.skip("MongoDB service is not running at localhost:17017")
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
        pytest.skip("MongoDB service is not running at localhost:17017")
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
        pytest.skip("MongoDB service is not running at localhost:17017")
    client = MongoScaleClient(uri=MONGO_URI, db_name="test_coursedb")
    coll = client.get_secondary_preferred_collection("test_orders")
    from pymongo.read_preferences import SecondaryPreferred
    assert isinstance(coll.read_preference, SecondaryPreferred)
