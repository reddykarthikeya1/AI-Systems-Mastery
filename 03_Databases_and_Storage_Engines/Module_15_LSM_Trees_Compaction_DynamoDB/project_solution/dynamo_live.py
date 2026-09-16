"""Module 15: Real DynamoDB Single-Table Design & Boto3 Operations (Track B).

Interacts with AWS DynamoDB / DynamoDB Local via boto3 to demonstrate:
1. Single-table design schema (PK: string, SK: string).
2. Global Secondary Indexes (GSI) for inverse lookups.
3. Strongly consistent reads vs eventually consistent reads.
4. Conditional expressions preventing concurrent overwrite anomalies.
5. BatchWriteItem and Query with key condition expressions.
"""

from __future__ import annotations


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
        endpoint_url: str = "http://localhost:18000",
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

    def delete_entity(self, pk: str, sk: str) -> None:
        """Delete one item by its full composite key.

        DynamoDB deletes are idempotent by design: removing a key that does not
        exist succeeds silently rather than erroring. That is what makes this
        safe to call in test setup without first checking existence.
        """
        table = self.resource.Table(self.table_name)
        table.delete_item(Key={"PK": pk, "SK": sk})

    def query_partition(self, pk: str, consistent_read: bool = False) -> list[dict[str, Any]]:
        table = self.resource.Table(self.table_name)
        from boto3.dynamodb.conditions import Key
        resp = table.query(
            KeyConditionExpression=Key("PK").eq(pk),
            ConsistentRead=consistent_read,
        )
        return resp.get("Items", [])
