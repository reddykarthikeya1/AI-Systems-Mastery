"""Reference solution — Problem 03: Network Delay Time

Pattern:    Dijkstra, single-source maximum
Complexity: Time O(E log V), Space O(V + E)
"""

from __future__ import annotations

from p01_dijkstra import dijkstra


def network_delay(n: int, times: list[tuple[int, int, int]], k: int) -> int:
    # Reuse Dijkstra on 0-based labels by shifting.
    edges = [(u - 1, v - 1, w) for u, v, w in times]
    dist = dijkstra(n, edges, k - 1)

    worst = max(dist)
    # The signal has arrived everywhere only when the LAST node has it.
    return -1 if worst == float("inf") else int(worst)
