"""Reference solution — Problem 05: Minimum Spanning Tree (Kruskal)

Pattern:    Sort edges + union-find
Complexity: Time O(E log E), Space O(V)
"""

from __future__ import annotations


def kruskal_mst(n: int, edges: list[tuple[int, int, int]]) -> int:
    parent = list(range(n))
    size = [1] * n

    def find(x: int) -> int:
        # Path compression, iterative so a long chain cannot blow the stack.
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def union(a: int, b: int) -> bool:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False            # already connected: this edge would cycle
        if size[ra] < size[rb]:     # union by size keeps trees shallow
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True

    total = 0
    taken = 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if union(u, v):
            total += w
            taken += 1
            if taken == n - 1:
                break

    return total if taken == n - 1 else -1
