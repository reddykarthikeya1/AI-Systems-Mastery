"""Reference solution — Problem 08: Minimum Cost To Connect All Points

Pattern:    MST on a complete graph
Complexity: Time O(n^2 log n), Space O(n)
"""

from __future__ import annotations


def min_cost_connect_points(points: list[tuple[int, int]]) -> int:
    import heapq

    n = len(points)
    if n <= 1:
        return 0

    # Prim over the implicit complete graph: keep the cheapest known cost to
    # reach each unvisited point, rather than materialising ~n^2/2 edges.
    in_tree = [False] * n
    best: list[int] = [0] + [10**18] * (n - 1)
    heap: list[tuple[int, int]] = [(0, 0)]
    total = 0
    count = 0

    while heap and count < n:
        cost, u = heapq.heappop(heap)
        if in_tree[u]:
            continue
        in_tree[u] = True
        total += cost
        count += 1
        ux, uy = points[u]
        for v in range(n):
            if in_tree[v]:
                continue
            vx, vy = points[v]
            d = abs(ux - vx) + abs(uy - vy)
            if d < best[v]:
                best[v] = d
                heapq.heappush(heap, (d, v))

    return total
