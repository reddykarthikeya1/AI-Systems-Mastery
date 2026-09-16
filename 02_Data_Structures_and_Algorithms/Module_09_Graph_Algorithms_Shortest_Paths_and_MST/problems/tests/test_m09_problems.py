"""Problem-bank suite for Module_09_Graph_Algorithms_Shortest_Paths_and_MST.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import pytest
from p01_dijkstra import dijkstra
from p02_bellman_ford import bellman_ford
from p03_network_delay import network_delay
from p04_cheapest_flights_k_stops import cheapest_flights
from p05_kruskal_mst import kruskal_mst
from p06_prim_mst import prim_mst
from p07_redundant_connection import redundant_connection
from p08_min_cost_connect_points import min_cost_connect_points


def test_p01_dijkstra():
    """Dijkstra's Shortest Paths — Dijkstra with a heap (Medium)."""
    assert dijkstra(3, [(0, 1, 4), (0, 2, 1), (2, 1, 2)], 0) == [0, 3, 1]
    # Unreachable nodes stay at infinity.
    assert dijkstra(3, [(0, 1, 1)], 0) == [0, 1, float('inf')]
    assert dijkstra(1, [], 0) == [0]
    # A zero-weight edge is legal.
    assert dijkstra(2, [(0, 1, 0)], 0) == [0, 0]
    # Parallel edges: the cheaper one must win.
    assert dijkstra(2, [(0, 1, 5), (0, 1, 2)], 0) == [0, 2]
    # A self-loop changes nothing.
    assert dijkstra(2, [(0, 0, 3), (0, 1, 1)], 0) == [0, 1]
    # The direct edge is not always the shortest route.
    assert dijkstra(4, [(0, 1, 10), (0, 2, 1), (2, 3, 1), (3, 1, 1)], 0) == [0, 3, 1, 2]
    # Starting elsewhere.
    assert dijkstra(3, [(0, 1, 1), (1, 2, 1)], 1) == [float('inf'), 0, 1]
    # Scale: a 50k chain.
    chain = [(i, i + 1, 1) for i in range(50_000)]
    d = dijkstra(50_001, chain, 0)
    assert d[-1] == 50_000 and d[0] == 0

def test_p02_bellman_ford():
    """Bellman-Ford With Negative Cycle Detection — Bellman-Ford (Hard)."""
    # A negative edge that Dijkstra would get wrong.
    assert bellman_ford(3, [(0, 1, 4), (0, 2, 1), (2, 1, -2)], 0) == [0, -1, 1]
    # A reachable negative cycle.
    assert bellman_ford(2, [(0, 1, 1), (1, 0, -3)], 0) is None
    assert bellman_ford(1, [], 0) == [0]
    # All non-negative: must agree with Dijkstra.
    edges = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5)]
    assert bellman_ford(4, edges, 0) == dijkstra(4, edges, 0)
    # Unreachable nodes stay at infinity.
    assert bellman_ford(3, [(0, 1, 2)], 0) == [0, 2, float('inf')]
    # An UNREACHABLE negative cycle is not an error - the source's own, # distances are still well defined.
    res = bellman_ford(4, [(0, 1, 1), (2, 3, -1), (3, 2, -1)], 0)
    assert res is not None
    assert res[0] == 0 and res[1] == 1
    # A negative self-loop is a negative cycle.
    assert bellman_ford(2, [(0, 1, 1), (1, 1, -1)], 0) is None
    # A single negative edge with no cycle is fine.
    assert bellman_ford(2, [(0, 1, -5)], 0) == [0, -5]

def test_p03_network_delay():
    """Network Delay Time — Dijkstra, single-source maximum (Medium)."""
    assert network_delay(4, [(2, 1, 1), (2, 3, 1), (3, 4, 1)], 2) == 2
    assert network_delay(2, [(1, 2, 1)], 1) == 1
    # Node 1 is unreachable from node 2.
    assert network_delay(2, [(1, 2, 1)], 2) == -1
    # A single node needs no time.
    assert network_delay(1, [], 1) == 0
    # It is the maximum, not the sum.
    assert network_delay(3, [(1, 2, 1), (1, 3, 5)], 1) == 5
    # A detour can beat the direct edge.
    assert network_delay(3, [(1, 2, 10), (1, 3, 1), (3, 2, 1)], 1) == 2
    # Zero-weight edges.
    assert network_delay(2, [(1, 2, 0)], 1) == 0
    # Disconnected node.
    assert network_delay(3, [(1, 2, 1)], 1) == -1

def test_p04_cheapest_flights_k_stops():
    """Cheapest Flight With At Most K Stops — Bellman-Ford by rounds (Hard)."""
    flights = [(0, 1, 100), (1, 2, 100), (2, 0, 100), (1, 3, 600), (2, 3, 200)]
    assert cheapest_flights(4, flights, 0, 3, 1) == 700
    assert cheapest_flights(4, flights, 0, 3, 2) == 400
    # k = 0 means a direct flight only.
    assert cheapest_flights(3, [(0, 1, 100), (1, 2, 100)], 0, 2, 0) == -1
    assert cheapest_flights(3, [(0, 1, 100), (0, 2, 500)], 0, 2, 0) == 500
    # One stop makes the cheaper two-leg route available.
    assert cheapest_flights(3, [(0, 1, 100), (1, 2, 100), (0, 2, 500)], 0, 2, 1) == 200
    # src == dst costs nothing.
    assert cheapest_flights(2, [], 0, 0, 0) == 0
    # No route at all.
    assert cheapest_flights(2, [], 0, 1, 1) == -1
    # The in-place-relaxation bug shows up here: relaxing in place
    # would chain both legs in round 1 and return 200 for k = 0.
    assert cheapest_flights(3, [(0, 1, 100), (1, 2, 100)], 0, 2, 0) == -1

def test_p05_kruskal_mst():
    """Minimum Spanning Tree (Kruskal) — Sort edges + union-find (Medium)."""
    assert kruskal_mst(4, [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 10)]) == 6
    # A single node needs no edges.
    assert kruskal_mst(1, []) == 0
    # Disconnected.
    assert kruskal_mst(3, [(0, 1, 1)]) == -1
    assert kruskal_mst(2, []) == -1
    # The cheaper of two parallel edges is used.
    assert kruskal_mst(2, [(0, 1, 5), (0, 1, 2)]) == 2
    # A cycle: the most expensive edge is skipped.
    assert kruskal_mst(3, [(0, 1, 1), (1, 2, 2), (0, 2, 100)]) == 3
    # Negative weights are still handled by the same greedy order.
    assert kruskal_mst(3, [(0, 1, -5), (1, 2, -3), (0, 2, 1)]) == -8
    # A star graph.
    assert kruskal_mst(4, [(0, 1, 1), (0, 2, 1), (0, 3, 1)]) == 3
    # Scale.
    chain = [(i, i + 1, 1) for i in range(99_999)]
    assert kruskal_mst(100_000, chain) == 99_999

def test_p06_prim_mst():
    """Minimum Spanning Tree (Prim) — Prim with a heap (Medium)."""
    assert prim_mst(4, [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 10)]) == 6
    assert prim_mst(1, []) == 0
    assert prim_mst(3, [(0, 1, 1)]) == -1
    assert prim_mst(2, [(0, 1, 5), (0, 1, 2)]) == 2
    assert prim_mst(3, [(0, 1, 1), (1, 2, 2), (0, 2, 100)]) == 3
    assert prim_mst(4, [(0, 1, 1), (0, 2, 1), (0, 3, 1)]) == 3
    # Prim and Kruskal must always agree on the total weight.
    cases = [
        (4, [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 10)]),
        (5, [(0, 1, 2), (0, 3, 6), (1, 2, 3), (1, 3, 8), (1, 4, 5), (2, 4, 7), (3, 4, 9)]),
        (3, [(0, 1, 1), (1, 2, 2), (0, 2, 100)]),
        (6, [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (3, 4, 2), (4, 5, 6)]),
        (3, [(0, 1, 1)]),
    ]
    for n_nodes, es in cases:
        assert prim_mst(n_nodes, es) == kruskal_mst(n_nodes, es), es

def test_p07_redundant_connection():
    """Redundant Connection — Union-find cycle detection (Medium)."""
    assert redundant_connection([(1, 2), (1, 3), (2, 3)]) == (2, 3)
    assert redundant_connection([(1, 2), (2, 3), (3, 4), (1, 4), (1, 5)]) == (1, 4)
    # A triangle at the end.
    assert redundant_connection([(1, 2), (2, 3), (1, 3)]) == (1, 3)
    # The cycle-closing edge is the first one whose ends already meet.
    assert redundant_connection([(1, 4), (3, 4), (1, 3), (1, 2)]) == (1, 3)
    # A genuine tree has no redundant edge.
    with pytest.raises(ValueError):
        redundant_connection([(1, 2), (2, 3)])
    # Removing the returned edge must leave a connected acyclic graph.
    for es in (
        [(1, 2), (1, 3), (2, 3)],
        [(1, 2), (2, 3), (3, 4), (1, 4), (1, 5)],
        [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5)],
    ):
        bad = redundant_connection(es)
        kept = [e for e in es if e != bad]
        nodes = {x for e in es for x in e}
        # A tree on k nodes has exactly k-1 edges...
        assert len(kept) == len(nodes) - 1
        # ...and is connected. Walk it to confirm.
        nbr: dict[int, list[int]] = {x: [] for x in nodes}
        for u, v in kept:
            nbr[u].append(v)
            nbr[v].append(u)
        start = next(iter(nodes))
        seen_nodes = {start}
        stack = [start]
        while stack:
            x = stack.pop()
            for y in nbr[x]:
                if y not in seen_nodes:
                    seen_nodes.add(y)
                    stack.append(y)
        assert seen_nodes == nodes, es

def test_p08_min_cost_connect_points():
    """Minimum Cost To Connect All Points — MST on a complete graph (Hard)."""
    assert min_cost_connect_points([(0, 0), (2, 2), (3, 10), (5, 2), (7, 0)]) == 20
    assert min_cost_connect_points([(3, 12), (-2, 5), (-4, 1)]) == 18
    assert min_cost_connect_points([(0, 0)]) == 0
    assert min_cost_connect_points([]) == 0
    # Two points: just the one edge.
    assert min_cost_connect_points([(0, 0), (1, 1)]) == 2
    # Collinear points connect along the line.
    assert min_cost_connect_points([(0, 0), (1, 0), (2, 0), (3, 0)]) == 3
    # Duplicate points cost nothing to connect.
    assert min_cost_connect_points([(1, 1), (1, 1), (1, 1)]) == 0
    # Cross-check against Kruskal on the explicit complete graph.
    pts = [(0, 0), (2, 2), (3, 10), (5, 2), (7, 0), (-1, 4)]
    explicit = [
        (i, j, abs(pts[i][0] - pts[j][0]) + abs(pts[i][1] - pts[j][1]))
        for i in range(len(pts))
        for j in range(i + 1, len(pts))
    ]
    assert min_cost_connect_points(pts) == kruskal_mst(len(pts), explicit)
