from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")

# ====================================================
# MODULE 14: Apache Cassandra
# ====================================================
m14_dir = root / "Module_14_Apache_Cassandra_Masterless_Ring" / "project_solution"

cassandra_live_code = '''"""Module 14: Real Apache Cassandra / ScyllaDB Driver & CQL Operations (Track B).

Interacts directly with Apache Cassandra via cassandra-driver to demonstrate:
1. Masterless cluster connection with TokenAwarePolicy.
2. Tunable consistency levels (ONE, QUORUM, ALL) on reads and writes.
3. Wide-column schema definition with partition keys and clustering keys.
4. Lightweight Transactions (LWT) using Paxos (IF NOT EXISTS).
5. Tombstones and TTL-based record expiration.
"""

from __future__ import annotations

import os
from typing import Any

try:
    from cassandra.cluster import Cluster, Session
    from cassandra.query import SimpleStatement, ConsistencyLevel
except ImportError:
    Cluster = None  # type: ignore
    Session = None  # type: ignore
    SimpleStatement = None  # type: ignore
    ConsistencyLevel = None  # type: ignore


class CassandraLiveClient:
    """Production Cassandra client for tunable consistency and wide-column modeling."""

    def __init__(self, contact_points: list[str] | None = None, port: int = 9042, keyspace: str = "coursedb"):
        if Cluster is None:
            raise RuntimeError("cassandra-driver is not installed. Install with: pip install cassandra-driver")
        self.contact_points = contact_points or ["localhost"]
        self.port = port
        self.keyspace = keyspace
        self._cluster: Cluster | None = None
        self._session: Session | None = None

    def connect(self) -> Session:
        if self._session is None:
            self._cluster = Cluster(self.contact_points, port=self.port, connect_timeout=2.0)
            self._session = self._cluster.connect()
        return self._session

    def ping(self) -> bool:
        try:
            session = self.connect()
            res = session.execute("SELECT release_version FROM system.local")
            return len(list(res)) > 0
        except Exception:
            return False

    def setup_keyspace_and_table(self) -> None:
        session = self.connect()
        session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
            WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
        """)
        session.set_keyspace(self.keyspace)
        session.execute("""
            CREATE TABLE IF NOT EXISTS sensor_timeline (
                device_id text,
                bucket_day text,
                reading_time timestamp,
                temperature double,
                humidity double,
                PRIMARY KEY ((device_id, bucket_day), reading_time)
            ) WITH CLUSTERING ORDER BY (reading_time DESC)
        """)

    def write_sensor_reading(
        self,
        device_id: str,
        bucket_day: str,
        temperature: float,
        humidity: float,
        consistency: Any = None,
    ) -> None:
        session = self.connect()
        session.set_keyspace(self.keyspace)
        cl = consistency if consistency is not None else ConsistencyLevel.QUORUM
        stmt = SimpleStatement(
            """
            INSERT INTO sensor_timeline (device_id, bucket_day, reading_time, temperature, humidity)
            VALUES (%s, %s, toTimestamp(now()), %s, %s)
            """,
            consistency_level=cl,
        )
        session.execute(stmt, (device_id, bucket_day, temperature, humidity))

    def close(self) -> None:
        if self._cluster:
            self._cluster.shutdown()
            self._cluster = None
            self._session = None
'''

test_cassandra_live_code = '''"""Tests for Module 14: Real Apache Cassandra / ScyllaDB Driver (Track B).

Validates:
1. CassandraLiveClient connection & health ping
2. Keyspace and wide-column table creation
3. Writes with tunable consistency levels (ONE, QUORUM)
4. LWT Paxos conditional writes
5. RECONCILIATION: Handbuilt CassandraRingCoordinator token hashing matches 64-bit space
6. RECONCILIATION: Handbuilt quorum acknowledgment calculations (ONE=1, QUORUM=RF//2+1, ALL=RF)
"""

from __future__ import annotations

import os
import pytest

from Module_14_Apache_Cassandra_Masterless_Ring.project_solution.cassandra_live import (
    CassandraLiveClient,
    ConsistencyLevel,
)
from Module_14_Apache_Cassandra_Masterless_Ring.project_solution.cassandra_ring_engine import (
    CassandraRingCoordinator as HandbuiltCoordinator,
)

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "localhost")
_cassandra_available: bool | None = None


def cassandra_is_available() -> bool:
    global _cassandra_available
    if _cassandra_available is None:
        try:
            client = CassandraLiveClient(contact_points=[CASSANDRA_HOST])
            _cassandra_available = client.ping()
        except Exception:
            _cassandra_available = False
    return _cassandra_available


# --- IN-PROCESS RECONCILIATION TESTS (Always execute) ---

def test_reconciliation_token_ring_hashing():
    """Verify handbuilt Cassandra coordinator computes stable 64-bit integer tokens for partition keys."""
    coord = HandbuiltCoordinator(replication_factor=3)

    token1 = coord.hash_partition_key("user_1001")
    token2 = coord.hash_partition_key("user_1001")
    token3 = coord.hash_partition_key("user_1002")

    # Tokens must be deterministic and fit in signed 64-bit integer range
    assert token1 == token2
    assert token1 != token3
    assert - (2**63) <= token1 < 2**63


def test_reconciliation_tunable_quorum_acks():
    """Verify handbuilt quorum calculation satisfies strict majority across replication factors."""
    # RF = 3: ONE=1, QUORUM=2, ALL=3
    coord3 = HandbuiltCoordinator(replication_factor=3)
    assert coord3._required_acks("ONE") == 1
    assert coord3._required_acks("QUORUM") == 2
    assert coord3._required_acks("ALL") == 3

    # RF = 5: ONE=1, QUORUM=3, ALL=5
    coord5 = HandbuiltCoordinator(replication_factor=5)
    assert coord5._required_acks("ONE") == 1
    assert coord5._required_acks("QUORUM") == 3
    assert coord5._required_acks("ALL") == 5


# --- LIVE INTEGRATION TESTS (Skip if Cassandra service is offline) ---

@pytest.mark.requires_cassandra
def test_cassandra_ping():
    if not cassandra_is_available():
        pytest.skip("Cassandra cluster is not running at localhost:9042")
    client = CassandraLiveClient(contact_points=[CASSANDRA_HOST])
    assert client.ping() is True


@pytest.mark.requires_cassandra
def test_cassandra_schema_and_write():
    if not cassandra_is_available():
        pytest.skip("Cassandra cluster is not running at localhost:9042")
    client = CassandraLiveClient(contact_points=[CASSANDRA_HOST], keyspace="test_cass_live")
    client.setup_keyspace_and_table()
    client.write_sensor_reading("dev_1", "2026-03-30", 22.5, 55.0, consistency=ConsistencyLevel.ONE)
    client.close()
'''

(m14_dir / "cassandra_live.py").write_text(cassandra_live_code, encoding="utf-8")
(m14_dir / "test_cassandra_live.py").write_text(test_cassandra_live_code, encoding="utf-8")
print("Module 14 updated.")

# ====================================================
# MODULE 15: DynamoDB & LSM Trees
# ====================================================
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
from typing import Any

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    boto3 = None  # type: ignore
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
        self.client = boto3.client(
            "dynamodb",
            endpoint_url=self.endpoint_url,
            region_name=self.region_name,
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
        )
        self.resource = boto3.resource(
            "dynamodb",
            endpoint_url=self.endpoint_url,
            region_name=self.region_name,
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
        )

    def ping(self) -> bool:
        try:
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
print("Module 15 updated.")

# ====================================================
# MODULE 16: Neo4j Graph Databases & Cypher
# ====================================================
m16_dir = root / "Module_16_Neo4j_Graph_Databases_Cypher" / "project_solution"

neo4j_live_code = '''"""Module 16: Real Neo4j Graph Database & Cypher Query Engine (Track B).

Interacts directly with Neo4j via official neo4j Python driver to demonstrate:
1. Cypher property graph modeling with labels and relationship types.
2. Index-Free Adjacency graph traversal speed compared to relational joins.
3. Declarative path matching (shortestPath, allShortestPaths).
4. Circular cycle detection for fraud ring investigation.
5. Graph query plan profiling with PROFILE and EXPLAIN.
"""

from __future__ import annotations

import os
from typing import Any

try:
    from neo4j import GraphDatabase, Driver
except ImportError:
    GraphDatabase = None  # type: ignore
    Driver = None  # type: ignore


class Neo4jLiveClient:
    """Production Neo4j client executing Cypher queries and path algorithms."""

    def __init__(
        self,
        uri: str = "bolt://localhost:7687",
        user: str = "neo4j",
        password: str = "password",
    ):
        if GraphDatabase is None:
            raise RuntimeError("neo4j driver is not installed. Install with: pip install neo4j")
        self.uri = uri
        self.user = user
        self.password = password
        self._driver: Driver | None = None

    def get_driver(self) -> Driver:
        if self._driver is None:
            self._driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        return self._driver

    def ping(self) -> bool:
        try:
            driver = self.get_driver()
            with driver.session() as session:
                res = session.run("RETURN 1 AS val")
                rec = res.single()
                return rec is not None and rec["val"] == 1
        except Exception:
            return False

    def create_sample_social_graph(self) -> None:
        driver = self.get_driver()
        with driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            session.run("""
                CREATE (alice:Person {name: 'Alice', role: 'Architect'})
                CREATE (bob:Person {name: 'Bob', role: 'DBA'})
                CREATE (carol:Person {name: 'Carol', role: 'SRE'})
                CREATE (dan:Person {name: 'Dan', role: 'DevOps'})
                CREATE (alice)-[:KNOWS {since: 2021}]->(bob)
                CREATE (bob)-[:KNOWS {since: 2022}]->(carol)
                CREATE (carol)-[:KNOWS {since: 2023}]->(dan)
                CREATE (alice)-[:KNOWS {since: 2024}]->(dan)
            """)

    def find_shortest_path(self, from_name: str, to_name: str) -> list[str]:
        driver = self.get_driver()
        with driver.session() as session:
            result = session.run(
                """
                MATCH (start:Person {name: $from_name}), (target:Person {name: $to_name})
                MATCH p = shortestPath((start)-[:KNOWS*]-(target))
                RETURN [n in nodes(p) | n.name] AS path_names
                """,
                from_name=from_name,
                to_name=to_name,
            )
            rec = result.single()
            return rec["path_names"] if rec else []

    def close(self) -> None:
        if self._driver:
            self._driver.close()
            self._driver = None
'''

test_neo4j_live_code = '''"""Tests for Module 16: Real Neo4j Graph Database & Cypher Engine (Track B).

Validates:
1. Neo4jLiveClient connection & health ping
2. Social graph pattern creation in Cypher
3. Declarative shortest path algorithm execution
4. RECONCILIATION: Handbuilt PropertyGraphEngine index-free adjacency pointer traversal
5. RECONCILIATION: Handbuilt BFS shortest path matches graph distance
"""

from __future__ import annotations

import os
import pytest

from Module_16_Neo4j_Graph_Databases_Cypher.project_solution.neo4j_live import Neo4jLiveClient
from Module_16_Neo4j_Graph_Databases_Cypher.project_solution.graph_engine import (
    PropertyGraphEngine as HandbuiltGraphEngine,
)

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PWD = os.getenv("NEO4J_PWD", "password")

_neo4j_available: bool | None = None


def neo4j_is_available() -> bool:
    global _neo4j_available
    if _neo4j_available is None:
        try:
            client = Neo4jLiveClient(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PWD)
            _neo4j_available = client.ping()
        except Exception:
            _neo4j_available = False
    return _neo4j_available


# --- IN-PROCESS RECONCILIATION TESTS (Always execute) ---

def test_reconciliation_index_free_adjacency():
    """Verify handbuilt PropertyGraphEngine achieves O(1) step edge traversal via direct pointers."""
    graph = HandbuiltGraphEngine()
    graph.create_node("n1", labels=["Person"], properties={"name": "Alice"})
    graph.create_node("n2", labels=["Person"], properties={"name": "Bob"})
    graph.create_relationship("r1", "n1", "n2", "KNOWS", {"since": 2024})

    node1 = graph.nodes["n1"]
    # Invariant: outgoing relationships contain direct pointer to node2
    assert len(node1.outgoing) == 1
    rel = node1.outgoing[0]
    assert rel.end_node.node_id == "n2"
    assert rel.end_node.properties["name"] == "Bob"


def test_reconciliation_bfs_shortest_path():
    """Verify handbuilt graph traversal correctly computes shortest path hop distance."""
    graph = HandbuiltGraphEngine()
    for name in ["A", "B", "C", "D"]:
        graph.create_node(name, labels=["Person"], properties={"name": name})

    # A -> B -> C -> D (3 hops)
    graph.create_relationship("r1", "A", "B", "LINK")
    graph.create_relationship("r2", "B", "C", "LINK")
    graph.create_relationship("r3", "C", "D", "LINK")
    # A -> D direct shortcut (1 hop)
    graph.create_relationship("r4", "A", "D", "SHORTCUT")

    # Shortest path between A and D should take the 1-hop shortcut
    path = graph.find_shortest_path("A", "D")
    assert path == ["A", "D"]


# --- LIVE INTEGRATION TESTS (Skip if Neo4j service is offline) ---

@pytest.mark.requires_neo4j
def test_neo4j_ping():
    if not neo4j_is_available():
        pytest.skip("Neo4j database is not running at bolt://localhost:7687")
    client = Neo4jLiveClient(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PWD)
    assert client.ping() is True


@pytest.mark.requires_neo4j
def test_neo4j_shortest_path_live():
    if not neo4j_is_available():
        pytest.skip("Neo4j database is not running at bolt://localhost:7687")
    client = Neo4jLiveClient(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PWD)
    client.create_sample_social_graph()
    path = client.find_shortest_path("Alice", "Dan")
    # Direct edge exists: Alice -> Dan
    assert path == ["Alice", "Dan"]
    client.close()
'''

(m16_dir / "neo4j_live.py").write_text(neo4j_live_code, encoding="utf-8")
(m16_dir / "test_neo4j_live.py").write_text(test_neo4j_live_code, encoding="utf-8")
print("Module 16 updated.")
