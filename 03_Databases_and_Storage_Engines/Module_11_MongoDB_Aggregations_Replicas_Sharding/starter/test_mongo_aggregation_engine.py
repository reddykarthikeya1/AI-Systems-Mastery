"""Automated pytest test suite for Module 11 MongoDB Aggregations & Sharding."""

import pytest
from mongo_aggregation_engine import AggregationPipeline, ShardRouter


@pytest.fixture
def sample_orders() -> list[dict]:
    return [
        {"order_id": 1, "customer": "Alice", "status": "COMPLETED", "items": [{"prod": "Laptop", "price": 1200}, {"prod": "Mouse", "price": 25}]},
        {"order_id": 2, "customer": "Bob", "status": "CANCELLED", "items": [{"prod": "Monitor", "price": 300}]},
        {"order_id": 3, "customer": "Charlie", "status": "COMPLETED", "items": [{"prod": "Keyboard", "price": 100}, {"prod": "Mouse", "price": 25}]},
        {"order_id": 4, "customer": "Alice", "status": "COMPLETED", "items": [{"prod": "Laptop", "price": 1200}]},
    ]


def test_aggregation_pipeline_full_chain(sample_orders: list[dict]) -> None:
    # Full pipeline: $match -> $unwind -> $group -> $sort -> $limit
    pipeline = (
        AggregationPipeline(sample_orders)
        .match({"status": "COMPLETED"})
        .unwind("items")
        .group("items.prod", {
            "total_revenue": ("$sum", "items.price"),
            "avg_price": ("$avg", "items.price"),
            "units_sold": ("$count", "items.price"),
        })
        .sort("total_revenue", descending=True)
        .limit(2)
    )

    results = pipeline.execute()
    assert len(results) == 2

    # Top product: Laptop (2 sales @ $1200 = $2400)
    assert results[0]["_id"] == "Laptop"
    assert results[0]["total_revenue"] == 2400.0
    assert results[0]["units_sold"] == 2

    # Second product: Keyboard ($100) or Mouse ($50)
    assert results[1]["_id"] == "Keyboard"
    assert results[1]["total_revenue"] == 100.0


def test_sharding_distribution_and_targeted_query() -> None:
    router = ShardRouter(num_shards=3, shard_key="customer_id")

    # Insert documents
    router.insert({"customer_id": "CUST_1", "name": "Alice", "status": "ACTIVE"})
    router.insert({"customer_id": "CUST_2", "name": "Bob", "status": "PENDING"})
    router.insert({"customer_id": "CUST_3", "name": "Charlie", "status": "ACTIVE"})

    # Targeted Query: includes shard key 'customer_id'
    results, was_targeted = router.query({"customer_id": "CUST_1"})
    assert len(results) == 1
    assert results[0]["name"] == "Alice"
    assert was_targeted is True  # Single shard direct route!


def test_sharding_scatter_gather_query() -> None:
    router = ShardRouter(num_shards=3, shard_key="customer_id")
    router.insert({"customer_id": "CUST_A", "status": "ACTIVE"})
    router.insert({"customer_id": "CUST_B", "status": "ACTIVE"})
    router.insert({"customer_id": "CUST_C", "status": "INACTIVE"})

    # Scatter-Gather Query: query by 'status' (no shard key)
    results, was_targeted = router.query({"status": "ACTIVE"})
    assert len(results) == 2
    assert was_targeted is False  # Broadcasted to all shards!


def test_missing_shard_key_raises_key_error() -> None:
    router = ShardRouter(num_shards=3, shard_key="customer_id")
    with pytest.raises(KeyError, match="missing required shard key: 'customer_id'"):
        router.insert({"name": "No Key Document"})
