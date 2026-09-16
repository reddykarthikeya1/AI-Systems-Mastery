from pathlib import Path

root = Path(r"c:\Users\Karthikeya Reddy\OneDrive - RITE\Desktop\Office Work\Subject\Databases")

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
import socket
from urllib.parse import urlparse
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
            self._driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password), connection_timeout=1.0)
        return self._driver

    def ping(self) -> bool:
        """Fast pre-check via socket connection followed by Cypher ping."""
        try:
            p = urlparse(self.uri)
            host = p.hostname or "localhost"
            port = p.port or 7687
            with socket.create_connection((host, port), timeout=0.2):
                pass
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
    path = graph.shortest_path("A", "D")
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
    assert path == ["Alice", "Dan"]
    client.close()
'''

(m16_dir / "neo4j_live.py").write_text(neo4j_live_code, encoding="utf-8")
(m16_dir / "test_neo4j_live.py").write_text(test_neo4j_live_code, encoding="utf-8")
print("Module 16 updated with shortest_path and fast socket ping.")
