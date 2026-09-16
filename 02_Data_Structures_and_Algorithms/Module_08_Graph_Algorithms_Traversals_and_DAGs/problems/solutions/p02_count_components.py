"""Reference solution — Problem 02: Count Connected Components

Pattern:    BFS/DFS over an adjacency list
Complexity: Time O(n + E), Space O(n + E)
"""

from __future__ import annotations


def count_components(n: int, edges: list[tuple[int, int]]) -> int:
    from collections import deque

    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)        # undirected: both directions

    seen = [False] * n
    components = 0

    for start in range(n):
        if seen[start]:
            continue
        # A node reached from nowhere begins a new component - including an
        # isolated node with no edges at all.
        components += 1
        seen[start] = True
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    queue.append(v)

    return components
