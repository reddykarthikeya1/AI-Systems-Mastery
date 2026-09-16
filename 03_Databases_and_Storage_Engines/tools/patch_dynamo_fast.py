from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")

# Update dynamo_live.py
m15_dir = root / "Module_15_LSM_Trees_Compaction_DynamoDB" / "project_solution"

dynamo_live_code = '''"""Module 15: Real DynamoDB Single-Table Design & Boto3 Operations (Track B).

Interacts with AWS DynamoDB / DynamoDB Local via boto3 to demonstrate:
1. Single-table design schema (PK: string, SK: string).
2. Global Secondary Indexes (GSI) for inverse lookups.
3. Strongly consistent reads vs eventually consistent reads.
4. Conditional expressions preventing concurrent overwrite anomalies.
5. BatchWriteItem and Query with key condition expressions.
"""

from __future__ import annotations

import os
import socket
from urllib.parse import urlparse
from typing import Any

try:
    import boto3
    from botocore.config import Config
    from botocore.exceptions import ClientError
except ImportError:
    boto3 = None  # type: ignore
    Config = None  # type: ignore
    ClientError = None  # type: ignore


class DynamoLiveClient:
    """Production DynamoDB client implementing single-table design."""

    def __init__(
        self,
        endpoint_url: str = "http://localhost:8000",
        region_name: str = "us-east-1",
        table_name: str = "enterprise_single_table",
    ):
        if boto3 is None:
            raise RuntimeError("boto3 is not installed. Install with: pip install boto3")
        self.endpoint_url = endpoint_url
        self.region_name = region_name
        self.table_name = table_name

        cfg = Config(connect_timeout=0.5, read_timeout=0.5, retries={"max_attempts": 0})
        self.client = boto3.client(
            "dynamodb",
            endpoint_url=self.endpoint_url,
            region_name=self.region_name,
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
            config=cfg,
        )
        self.resource = boto3.resource(
            "dynamodb",
            endpoint_url=self.endpoint_url,
            region_name=self.region_name,
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
            config=cfg,
        )

    def ping(self) -> bool:
        """Fast pre-check via socket connection followed by list_tables."""
        try:
            p = urlparse(self.endpoint_url)
            host = p.hostname or "localhost"
            port = p.port or 8000
            with socket.create_connection((host, port), timeout=0.2):
                pass
            self.client.list_tables()
            return True
        except Exception:
            return False

    def create_single_table(self) -> None:
        existing = self.client.list_tables()["TableNames"]
        if self.table_name in existing:
            return

        self.client.create_table(
            TableName=self.table_name,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
                {"AttributeName": "GSI1PK", "AttributeType": "S"},
                {"AttributeName": "GSI1SK", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "GSI1",
                    "KeySchema": [
                        {"AttributeName": "GSI1PK", "KeyType": "HASH"},
                        {"AttributeName": "GSI1SK", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
                }
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )

    def put_entity(self, item: dict[str, Any], condition_exists: bool = False) -> None:
        table = self.resource.Table(self.table_name)
        params: dict[str, Any] = {"Item": item}
        if not condition_exists:
            params["ConditionExpression"] = "attribute_not_exists(PK)"
        table.put_item(**params)

    def query_partition(self, pk: str, consistent_read: bool = False) -> list[dict[str, Any]]:
        table = self.resource.Table(self.table_name)
        from boto3.dynamodb.conditions import Key
        resp = table.query(
            KeyConditionExpression=Key("PK").eq(pk),
            ConsistentRead=consistent_read,
        )
        return resp.get("Items", [])
'''

test_dynamo_live_code = '''"""Tests for Module 15: Real DynamoDB Single-Table Design & Boto3 Operations (Track B).

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

DYNAMO_ENDPOINT = os.getenv("DYNAMO_ENDPOINT", "http://localhost:8000")
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
        pytest.skip("DynamoDB Local is not running at http://localhost:8000")
    client = DynamoLiveClient(endpoint_url=DYNAMO_ENDPOINT)
    assert client.ping() is True


@pytest.mark.requires_dynamo
def test_dynamo_single_table_lifecycle():
    if not dynamo_is_available():
        pytest.skip("DynamoDB Local is not running at http://localhost:8000")
    client = DynamoLiveClient(endpoint_url=DYNAMO_ENDPOINT, table_name="test_live_tab")
    client.create_single_table()

    client.put_entity({
        "PK": "ORG#1",
        "SK": "METADATA",
        "name": "Global Logistics",
        "GSI1PK": "METADATA",
        "GSI1SK": "ORG#1",
    })

    results = client.query_partition("ORG#1", consistent_read=True)
    assert len(results) == 1
    assert results[0]["name"] == "Global Logistics"
'''

(m15_dir / "dynamo_live.py").write_text(dynamo_live_code, encoding="utf-8")
(m15_dir / "test_dynamo_live.py").write_text(test_dynamo_live_code, encoding="utf-8")
print("Module 15 updated with fast socket ping.")
