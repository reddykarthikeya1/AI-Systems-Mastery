"""Reference solution - Problem 04: Edge-Disjoint Paths

Pattern:    Unit-capacity flow
Complexity: Time O(V * E^2)
"""

from __future__ import annotations

from collections import deque

INF = float("inf")


def _build(nodes, edges):
    graph = [[] for _ in range(nodes)]
    to, cap = [], []
    for a, b, c in edges:
        graph[a].append(len(to))
        to.append(b)
        cap.append(c)
        graph[b].append(len(to))
        to.append(a)
        cap.append(0)
    return graph, to, cap


def _max_flow(graph, to, cap, source, sink):
    total = 0
    while True:
        parent = [-1] * len(graph)
        parent[source] = -2
        queue = deque([source])
        while queue and parent[sink] == -1:
            node = queue.popleft()
            for edge_id in graph[node]:
                nxt = to[edge_id]
                if parent[nxt] == -1 and cap[edge_id] > 0:
                    parent[nxt] = edge_id
                    queue.append(nxt)
        if parent[sink] == -1:
            return total
        bottleneck = INF
        node = sink
        while node != source:
            edge_id = parent[node]
            bottleneck = min(bottleneck, cap[edge_id])
            node = to[edge_id ^ 1]
        node = sink
        while node != source:
            edge_id = parent[node]
            cap[edge_id] -= bottleneck
            cap[edge_id ^ 1] += bottleneck
            node = to[edge_id ^ 1]
        total += bottleneck


def edge_disjoint_paths(nodes: int, edges: list[tuple[int, int]],
                        source: int, sink: int) -> int:
    graph, to, cap = _build(nodes, [(a, b, 1) for a, b in edges])
    return _max_flow(graph, to, cap, source, sink)
