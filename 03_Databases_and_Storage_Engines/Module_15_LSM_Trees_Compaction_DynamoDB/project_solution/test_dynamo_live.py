"""Tests for Module 15: Real DynamoDB Single-Table Design & Boto3 Operations (Track B).

Validates:
1. DynamoLiveClient connection & health ping
2. Single-table creation with PK/SK and GSI1
3. Conditional write idempotency
4. Query partition with strongly consistent reads
5. RECONCILIATION: Handbuilt BloomFilter zero false negative guarantee
6. RECONCILIATION: Handbuilt DynamoDBSingleTableEngine PK/SK partition lookups
"""

from __future__ import annotations

import os
import pytest

from Module_15_LSM_Trees_Compaction_DynamoDB.project_solution.dynamo_live import DynamoLiveClient
from Module_15_LSM_Trees_Compaction_DynamoDB.project_solution.lsm_dynamo_engine import (
    BloomFilter as HandbuiltBloomFilter,
    DynamoDBSingleTableEngine as HandbuiltDynamoEngine,
)

DYNAMO_ENDPOINT = os.getenv("DYNAMO_ENDPOINT", "http://localhost:18000")
_dynamo_available: bool | None = None


def dynamo_is_available() -> bool:
    global _dynamo_available
    if _dynamo_available is None:
        try:
            client = DynamoLiveClient(endpoint_url=DYNAMO_ENDPOINT)
            _dynamo_available = client.ping()
        except Exception:
            _dynamo_available = False
    return _dynamo_available


# --- IN-PROCESS RECONCILIATION TESTS (Always execute) ---

def test_reconciliation_bloom_filter_zero_false_negatives():
    """Verify handbuilt BloomFilter has 0% false negative rate on all inserted elements."""
    bf = HandbuiltBloomFilter(expected_items=50, false_positive_rate=0.01)
    inserted_keys = [f"key_{i}" for i in range(50)]

    for k in inserted_keys:
        bf.add(k)

    # Invariant: Every inserted key MUST be reported present (no false negatives)
    for k in inserted_keys:
        assert bf.contains(k) is True


def test_reconciliation_single_table_partition_query():
    """Verify handbuilt DynamoDBSingleTableEngine PK/SK query returns exactly partition items."""
    engine = HandbuiltDynamoEngine()

    # Insert Customer entity
    engine.put_item({
        "PK": "CUST#101",
        "SK": "METADATA",
        "name": "Acme Corp",
        "email": "contact@acme.com",
    })
    # Insert Order entities under same partition
    engine.put_item({"PK": "CUST#101", "SK": "ORD#2026-001", "total": 1500.0})
    engine.put_item({"PK": "CUST#101", "SK": "ORD#2026-002", "total": 3200.0})

    # Query entire customer partition
    items = engine.query(pk="CUST#101")
    assert len(items) == 3
    sks = {it["SK"] for it in items}
    assert sks == {"METADATA", "ORD#2026-001", "ORD#2026-002"}


# --- LIVE INTEGRATION TESTS (Skip if DynamoDB Local service is offline) ---

@pytest.mark.requires_dynamo
def test_dynamo_ping():
    if not dynamo_is_available():
        pytest.skip("DynamoDB Local is not running at http://localhost:18000")
    client = DynamoLiveClient(endpoint_url=DYNAMO_ENDPOINT)
    assert client.ping() is True


@pytest.mark.requires_dynamo
def test_dynamo_single_table_lifecycle():
    if not dynamo_is_available():
        pytest.skip("DynamoDB Local is not running at http://localhost:18000")
    client = DynamoLiveClient(endpoint_url=DYNAMO_ENDPOINT, table_name="test_live_tab")
    client.create_single_table()

    item = {
        "PK": "ORG#1",
        "SK": "METADATA",
        "name": "Global Logistics",
        "GSI1PK": "METADATA",
        "GSI1SK": "ORG#1",
    }

    # `put_entity` guards with `attribute_not_exists(PK)` - the correct DynamoDB
    # idempotency pattern. That makes the write reject a duplicate, which also
    # means this test cannot re-run unless it cleans up first. A test that only
    # passes on a fresh database is a test that fails the moment CI retries.
    client.delete_entity("ORG#1", "METADATA")
    client.put_entity(item)

    # The guard must actually guard: a second unconditional insert of the same
    # key has to be refused, not silently overwrite.
    with pytest.raises(Exception, match="ConditionalCheckFailed"):
        client.put_entity(item)

    results = client.query_partition("ORG#1", consistent_read=True)
    assert len(results) == 1
    assert results[0]["name"] == "Global Logistics"
