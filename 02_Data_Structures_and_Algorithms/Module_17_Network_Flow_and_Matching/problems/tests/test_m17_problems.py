"""Problem-bank suite for Module_17_Network_Flow_and_Matching.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs - which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import itertools
import random

from p01_max_flow_value import max_flow_value
from p02_min_cut_edges import min_cut_edges
from p03_bipartite_matching import max_matching
from p04_edge_disjoint_paths import edge_disjoint_paths
from p05_vertex_disjoint_paths import vertex_disjoint_paths
from p06_assign_with_capacity import staff_shifts

DIAMOND = [(0, 1, 10), (1, 3, 3), (0, 2, 5), (2, 3, 5)]
CLRS = [(0, 1, 16), (0, 2, 13), (1, 2, 10), (1, 3, 12),
        (2, 1, 4), (2, 4, 14), (3, 2, 9), (3, 5, 20), (4, 3, 7), (4, 5, 4)]


def test_p01_max_flow_value():
    """Maximum Flow - Edmonds-Karp (Medium)."""
    assert max_flow_value(4, DIAMOND, 0, 3) == 8
    assert max_flow_value(6, CLRS, 0, 5) == 23
    # Bottleneck in the middle of a single chain.
    assert max_flow_value(4, [(0, 1, 10), (1, 2, 3), (2, 3, 10)], 0, 3) == 3
    # No route at all.
    assert max_flow_value(4, [(0, 1, 5), (2, 3, 5)], 0, 3) == 0
    assert max_flow_value(2, [], 0, 1) == 0
    # Zero-capacity edges carry nothing.
    assert max_flow_value(3, [(0, 1, 0), (1, 2, 5)], 0, 2) == 0
    # The graph that needs flow to be taken back again.
    reroute = [(0, 1, 1), (0, 2, 1), (1, 2, 1), (1, 3, 1), (2, 3, 1)]
    assert max_flow_value(4, reroute, 0, 3) == 2
    # Parallel edges add up.
    assert max_flow_value(2, [(0, 1, 3), (0, 1, 4)], 0, 1) == 7


def test_p02_min_cut_edges():
    """Which Edges Are the Bottleneck? - Max-flow min-cut (Hard)."""
    # Several minimum cuts exist here, all worth 8. Residual exploration from
    # the source yields this one - the source-minimal cut.
    assert min_cut_edges(4, DIAMOND, 0, 3) == [(0, 2), (1, 3)]
    assert sum(c for a, b, c in DIAMOND if (a, b) in [(0, 2), (1, 3)]) == 8

    # The theorem: the cut's capacity equals the max flow, on random graphs.
    random.seed(1702)
    for _ in range(120):
        nodes = random.randint(2, 7)
        edges = [(a, b, random.randint(1, 6))
                 for a in range(nodes) for b in range(nodes)
                 if a != b and random.random() < 0.4]
        sink = nodes - 1
        flow = max_flow_value(nodes, edges, 0, sink)
        cut = min_cut_edges(nodes, edges, 0, sink)
        assert sum(c for a, b, c in edges if (a, b) in cut) == flow
        # And removing exactly those edges must disconnect the sink.
        survivors = [(a, b, c) for a, b, c in edges if (a, b) not in cut]
        assert max_flow_value(nodes, survivors, 0, sink) == 0


def test_p03_bipartite_matching():
    """Maximum Bipartite Matching - Unit-capacity flow (Medium)."""
    assert max_matching(2, 2, [(0, 0), (0, 1), (1, 0)]) == 2
    assert max_matching(3, 3, [(0, 0), (1, 1), (2, 2)]) == 3
    assert max_matching(2, 2, []) == 0
    assert max_matching(3, 1, [(0, 0), (1, 0), (2, 0)]) == 1
    # Against an exhaustive search on small inputs.
    random.seed(1703)
    for _ in range(120):
        left = random.randint(1, 4)
        right = random.randint(1, 4)
        pairs = [(a, b) for a in range(left) for b in range(right)
                 if random.random() < 0.5]
        best = 0
        for size in range(min(left, right), 0, -1):
            if any(len({a for a, _ in c}) == size and len({b for _, b in c}) == size
                   for c in itertools.combinations(pairs, size)):
                best = size
                break
        assert max_matching(left, right, pairs) == best


def test_p04_edge_disjoint_paths():
    """Edge-Disjoint Paths - Unit-capacity flow (Medium)."""
    edges = [(0, 1), (1, 3), (0, 2), (2, 3), (0, 3)]
    assert edge_disjoint_paths(4, edges, 0, 3) == 3
    assert edge_disjoint_paths(4, [(0, 1), (1, 2), (2, 3)], 0, 3) == 1
    assert edge_disjoint_paths(3, [(0, 1)], 0, 2) == 0
    # A shared edge caps it at one however many routes appear to exist.
    shared = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
    assert edge_disjoint_paths(5, shared, 0, 4) == 1


def test_p05_vertex_disjoint_paths():
    """Vertex-Disjoint Paths - Node splitting (Hard)."""
    edges = [(0, 1), (1, 3), (0, 2), (2, 3), (0, 3)]
    assert vertex_disjoint_paths(4, edges, 0, 3) == 3
    # Both routes must pass through node 2, so only one may.
    funnel = [(0, 1), (1, 2), (2, 4), (0, 3), (3, 2)]
    assert vertex_disjoint_paths(5, funnel, 0, 4) == 1
    # Vertex-disjoint is never more than edge-disjoint.
    random.seed(1705)
    for _ in range(80):
        nodes = random.randint(2, 7)
        pairs = [(a, b) for a in range(nodes) for b in range(nodes)
                 if a != b and random.random() < 0.35]
        sink = nodes - 1
        assert (vertex_disjoint_paths(nodes, pairs, 0, sink)
                <= edge_disjoint_paths(nodes, pairs, 0, sink))


def test_p06_assign_with_capacity():
    """Workers Who Can Take Several Shifts - Flow with non-unit capacities."""
    available = [(0, 0), (0, 1), (1, 2), (1, 3)]
    assert staff_shifts(2, 4, available, shifts_each=2) == 4
    assert staff_shifts(2, 4, available, shifts_each=1) == 2
    assert staff_shifts(2, 4, available, shifts_each=5) == 4, "capped by the shifts"
    assert staff_shifts(1, 3, [(0, 0), (0, 1), (0, 2)], shifts_each=3) == 3
    assert staff_shifts(2, 2, [], shifts_each=2) == 0
    # With shifts_each = 1 it must agree with plain matching.
    random.seed(1706)
    for _ in range(80):
        workers = random.randint(1, 4)
        shifts = random.randint(1, 4)
        pairs = [(w, s) for w in range(workers) for s in range(shifts)
                 if random.random() < 0.5]
        assert (staff_shifts(workers, shifts, pairs, shifts_each=1)
                == max_matching(workers, shifts, pairs))
