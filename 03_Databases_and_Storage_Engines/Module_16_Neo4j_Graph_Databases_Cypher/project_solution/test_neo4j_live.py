"""Tests for Module 16: Real Neo4j Graph Database & Cypher Engine (Track B).

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

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:17687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PWD = os.getenv("NEO4J_PWD", "coursepw123")

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
        pytest.skip("Neo4j database is not running at bolt://localhost:17687")
    client = Neo4jLiveClient(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PWD)
    assert client.ping() is True


@pytest.mark.requires_neo4j
def test_neo4j_shortest_path_live():
    if not neo4j_is_available():
        pytest.skip("Neo4j database is not running at bolt://localhost:17687")
    client = Neo4jLiveClient(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PWD)
    client.create_sample_social_graph()
    path = client.find_shortest_path("Alice", "Dan")
    assert path == ["Alice", "Dan"]
    client.close()
