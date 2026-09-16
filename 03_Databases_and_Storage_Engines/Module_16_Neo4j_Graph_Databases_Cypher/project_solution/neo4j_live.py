"""Module 16: Real Neo4j Graph Database & Cypher Query Engine (Track B).

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

try:
    from neo4j import GraphDatabase, Driver
except ImportError:
    GraphDatabase = None  # type: ignore
    Driver = None  # type: ignore


class Neo4jLiveClient:
    """Production Neo4j client executing Cypher queries and path algorithms."""

    def __init__(
        self,
        uri: str = "bolt://localhost:17687",
        user: str = "neo4j",
        password: str = os.environ.get("NEO4J_PWD", "coursepw123"),
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
