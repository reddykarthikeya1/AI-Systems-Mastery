"""Reference solution - Problem 05: Vertex-Disjoint Paths

Pattern:    Node splitting
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


def vertex_disjoint_paths(nodes: int, edges: list[tuple[int, int]],
                          source: int, sink: int) -> int:
    # Node v becomes v_in = v and v_out = v + nodes.
    BIG = 10 ** 9
    split = []
    for v in range(nodes):
        capacity = BIG if v in (source, sink) else 1
        split.append((v, v + nodes, capacity))
    split += [(a + nodes, b, 1) for a, b in edges]
    graph, to, cap = _build(2 * nodes, split)
    return _max_flow(graph, to, cap, source, sink + nodes)
