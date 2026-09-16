"""Module 16: Neo4j & Graph Database Engine (Solution).

This is a pure-Python MODEL of graph storage with index-free adjacency and Cypher-style pattern matching, built to make the
mechanism visible. It does not connect to Neo4j. For the real driver,
real queries and real operational behaviour, see `neo4j_live.py`.

Implements:
1. GraphNode and GraphRelationship with native Index-Free Adjacency (direct pointer links).
2. Declarative pattern matching with label and property constraints.
3. Breadth-First Search (BFS) Shortest Path discovery.
4. Circular fraud ring cycle detection.
5. PageRank centrality calculation.
"""

from __future__ import annotations

from collections import deque
from typing import Any


class GraphNode:
    """A graph node with direct pointer links to incoming and outgoing relationships."""

    def __init__(self, node_id: str, labels: set[str], properties: dict[str, Any]) -> None:
        self.node_id = node_id
        self.labels = labels
        self.properties = properties
        self.outgoing: list[GraphRelationship] = []
        self.incoming: list[GraphRelationship] = []

    def __repr__(self) -> str:
        return f"Node({self.node_id}, labels={self.labels}, props={self.properties})"


class GraphRelationship:
    """A directed, typed relationship edge connecting two nodes directly via pointers."""

    def __init__(
        self,
        rel_id: str,
        rel_type: str,
        start_node: GraphNode,
        end_node: GraphNode,
        properties: dict[str, Any],
    ) -> None:
        self.rel_id = rel_id
        self.rel_type = rel_type
        self.start_node = start_node
        self.end_node = end_node
        self.properties = properties

    def __repr__(self) -> str:
        return f"Rel({self.rel_id}, :{self.rel_type}, {self.start_node.node_id}->{self.end_node.node_id})"


class PropertyGraphEngine:
    """In-memory property graph engine implementing Index-Free Adjacency."""

    def __init__(self) -> None:
        self.nodes: dict[str, GraphNode] = {}
        self.relationships: dict[str, GraphRelationship] = {}

    def create_node(self, node_id: str, labels: list[str] | set[str], properties: dict[str, Any]) -> GraphNode:
        if node_id in self.nodes:
            raise ValueError(f"Node '{node_id}' already exists in graph")
        node = GraphNode(node_id=node_id, labels=set(labels), properties=dict(properties))
        self.nodes[node_id] = node
        return node

    def create_relationship(
        self,
        rel_id: str,
        start_id: str,
        end_id: str,
        rel_type: str,
        properties: dict[str, Any] | None = None,
    ) -> GraphRelationship:
        if rel_id in self.relationships:
            raise ValueError(f"Relationship '{rel_id}' already exists")
        if start_id not in self.nodes or end_id not in self.nodes:
            raise KeyError(f"Both start '{start_id}' and end '{end_id}' nodes must exist")

        start_node = self.nodes[start_id]
        end_node = self.nodes[end_id]

        rel = GraphRelationship(
            rel_id=rel_id,
            rel_type=rel_type,
            start_node=start_node,
            end_node=end_node,
            properties=dict(properties or {}),
        )

        # Index-Free Adjacency: attach direct pointers to node's edge lists
        start_node.outgoing.append(rel)
        end_node.incoming.append(rel)
        self.relationships[rel_id] = rel
        return rel

    def match_pattern(
        self,
        start_label: str | None = None,
        rel_type: str | None = None,
        end_label: str | None = None,
        where_props: dict[str, Any] | None = None,
    ) -> list[tuple[GraphNode, GraphRelationship, GraphNode]]:
        matches: list[tuple[GraphNode, GraphRelationship, GraphNode]] = []

        candidate_nodes = [
            n for n in self.nodes.values()
            if start_label is None or start_label in n.labels
        ]

        for node in candidate_nodes:
            # Direct pointer traversal (O(1) per relationship)
            for rel in node.outgoing:
                if rel_type is not None and rel.rel_type != rel_type:
                    continue

                target_node = rel.end_node
                if end_label is not None and end_label not in target_node.labels:
                    continue

                if where_props:
                    match = True
                    for k, v in where_props.items():
                        if rel.properties.get(k) != v and target_node.properties.get(k) != v:
                            match = False
                            break
                    if not match:
                        continue

                matches.append((node, rel, target_node))

        return matches

    def shortest_path(
        self,
        start_id: str,
        target_id: str,
        rel_type: str | None = None,
        max_depth: int = 10,
    ) -> list[str] | None:
        if start_id not in self.nodes or target_id not in self.nodes:
            return None

        if start_id == target_id:
            return [start_id]

        visited: set[str] = {start_id}
        queue: deque[list[str]] = deque([[start_id]])

        while queue:
            path = queue.popleft()
            if len(path) > max_depth:
                continue

            current_node = self.nodes[path[-1]]
            for rel in current_node.outgoing:
                if rel_type is not None and rel.rel_type != rel_type:
                    continue

                neighbor_id = rel.end_node.node_id
                if neighbor_id == target_id:
                    return path + [neighbor_id]

                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append(path + [neighbor_id])

        return None

    def find_cycles(
        self,
        start_id: str,
        min_length: int = 3,
        max_length: int = 6,
    ) -> list[list[str]]:
        if start_id not in self.nodes:
            return []

        cycles: list[list[str]] = []
        queue: deque[list[str]] = deque([[start_id]])

        while queue:
            path = queue.popleft()
            current_node = self.nodes[path[-1]]

            for rel in current_node.outgoing:
                neighbor_id = rel.end_node.node_id
                if neighbor_id == start_id and len(path) >= min_length:
                    cycles.append(path + [start_id])
                elif neighbor_id not in path and len(path) < max_length:
                    queue.append(path + [neighbor_id])

        return cycles

    def pagerank(self, damping: float = 0.85, max_iterations: int = 20) -> dict[str, float]:
        n = len(self.nodes)
        if n == 0:
            return {}

        pr: dict[str, float] = {nid: 1.0 / n for nid in self.nodes}

        for _ in range(max_iterations):
            new_pr: dict[str, float] = {}
            for nid, node in self.nodes.items():
                incoming_sum = 0.0
                for rel in node.incoming:
                    source_node = rel.start_node
                    out_degree = len(source_node.outgoing)
                    if out_degree > 0:
                        incoming_sum += pr[source_node.node_id] / out_degree

                new_pr[nid] = ((1.0 - damping) / n) + (damping * incoming_sum)

            pr = new_pr

        # Normalize so sum equals 1.0
        total = sum(pr.values())
        if total > 0:
            pr = {k: v / total for k, v in pr.items()}

        return pr
