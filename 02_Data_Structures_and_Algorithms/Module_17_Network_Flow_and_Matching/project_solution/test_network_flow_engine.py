"""Tests for the network flow engine.

Two independent max-flow algorithms are cross-checked against each other on
randomised graphs, and bipartite matching is checked against an exhaustive
search on small inputs. Agreement between two different algorithms and a brute
force is much stronger evidence than any single hand-written expectation.
"""

from __future__ import annotations

import itertools
import random
import time

import pytest
from network_flow_engine import (
    FlowNetwork,
    bipartite_matching,
    dinic,
    edmonds_karp,
    greedy_matching,
    max_profit_projects,
    min_cut,
)


def build(nodes: int, edges: list[tuple[int, int, int]]) -> FlowNetwork:
    network = FlowNetwork(nodes)
    for source, target, capacity in edges:
        network.add_edge(source, target, capacity)
    return network


CLRS_EXAMPLE = [
    (0, 1, 16), (0, 2, 13),
    (1, 2, 10), (1, 3, 12),
    (2, 1, 4), (2, 4, 14),
    (3, 2, 9), (3, 5, 20),
    (4, 3, 7), (4, 5, 4),
]


# ---------------------------------------------------------------------------
# known answers
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("algorithm", [edmonds_karp, dinic])
def test_textbook_network(algorithm):
    # The standard worked example; the answer is 23.
    assert algorithm(build(6, CLRS_EXAMPLE), 0, 5) == 23


@pytest.mark.parametrize("algorithm", [edmonds_karp, dinic])
def test_single_path_is_limited_by_its_bottleneck(algorithm):
    assert algorithm(build(4, [(0, 1, 10), (1, 2, 3), (2, 3, 10)]), 0, 3) == 3


@pytest.mark.parametrize("algorithm", [edmonds_karp, dinic])
def test_disconnected_sink_has_no_flow(algorithm):
    assert algorithm(build(4, [(0, 1, 5), (2, 3, 5)]), 0, 3) == 0


@pytest.mark.parametrize("algorithm", [edmonds_karp, dinic])
def test_parallel_paths_add_up(algorithm):
    edges = [(0, 1, 5), (1, 3, 5), (0, 2, 7), (2, 3, 7)]
    assert algorithm(build(4, edges), 0, 3) == 12


@pytest.mark.parametrize("algorithm", [edmonds_karp, dinic])
def test_source_equal_to_sink_is_rejected(algorithm):
    with pytest.raises(ValueError):
        algorithm(build(2, []), 0, 0)


def test_negative_capacity_is_rejected():
    with pytest.raises(ValueError):
        build(2, [(0, 1, -1)])


# ---------------------------------------------------------------------------
# the residual edge is what makes it correct
# ---------------------------------------------------------------------------


def test_flow_must_be_undone_to_reach_the_optimum():
    """The graph where a greedy first choice is wrong.

    Taking 0->1->2->3 first saturates the middle edge and appears to block the
    other routes. Only the backward residual edge lets the algorithm push flow
    back through 1->2 and reroute, reaching 2 instead of 1.
    """
    edges = [(0, 1, 1), (0, 2, 1), (1, 2, 1), (1, 3, 1), (2, 3, 1)]
    assert dinic(build(4, edges), 0, 3) == 2
    assert edmonds_karp(build(4, edges), 0, 3) == 2


# ---------------------------------------------------------------------------
# differential: two algorithms must agree
# ---------------------------------------------------------------------------


def test_edmonds_karp_and_dinic_agree_on_random_graphs():
    random.seed(17)
    for _ in range(300):
        nodes = random.randint(2, 8)
        edges = []
        for source in range(nodes):
            for target in range(nodes):
                if source != target and random.random() < 0.35:
                    edges.append((source, target, random.randint(1, 9)))
        sink = nodes - 1
        a = edmonds_karp(build(nodes, edges), 0, sink)
        b = dinic(build(nodes, edges), 0, sink)
        assert a == b, f"disagreement on {nodes} nodes, edges={edges}"


# ---------------------------------------------------------------------------
# max-flow equals min-cut
# ---------------------------------------------------------------------------


def test_min_cut_value_equals_max_flow():
    random.seed(171)
    for _ in range(200):
        nodes = random.randint(2, 7)
        edges = []
        for source in range(nodes):
            for target in range(nodes):
                if source != target and random.random() < 0.4:
                    edges.append((source, target, random.randint(1, 6)))
        sink = nodes - 1
        flow = dinic(build(nodes, edges), 0, sink)
        value, _ = min_cut(build(nodes, edges), 0, sink)
        assert value == flow


def test_min_cut_edges_really_disconnect_the_sink():
    value, crossing = min_cut(build(6, CLRS_EXAMPLE), 0, 5)
    assert value == 23

    # Remove exactly those edges and no flow can get through at all.
    survivors = [(a, b, c) for (a, b, c) in CLRS_EXAMPLE if (a, b) not in crossing]
    assert dinic(build(6, survivors), 0, 5) == 0

    # And their capacities sum to the cut value: that is the theorem.
    assert sum(c for (a, b, c) in CLRS_EXAMPLE if (a, b) in crossing) == value


def test_min_cut_is_repeatable_on_the_same_network():
    network = build(6, CLRS_EXAMPLE)
    first = min_cut(network, 0, 5)
    second = min_cut(network, 0, 5)
    assert first == second, "min_cut must reset the network, not accumulate flow"


# ---------------------------------------------------------------------------
# bipartite matching
# ---------------------------------------------------------------------------


def brute_force_matching(left: int, right: int,
                         edges: list[tuple[int, int]]) -> int:
    """Largest valid matching, by trying every subset. Only for tiny inputs."""
    best = 0
    for size in range(len(edges), 0, -1):
        if size <= best:
            break
        for subset in itertools.combinations(edges, size):
            lefts = [a for a, _ in subset]
            rights = [b for _, b in subset]
            if len(set(lefts)) == size and len(set(rights)) == size:
                best = max(best, size)
                break
    return best


def test_bipartite_matching_matches_brute_force():
    random.seed(1717)
    for _ in range(150):
        left = random.randint(1, 4)
        right = random.randint(1, 4)
        edges = [(a, b) for a in range(left) for b in range(right)
                 if random.random() < 0.5]
        found = bipartite_matching(left, right, edges)
        assert len(found) == brute_force_matching(left, right, edges)
        # And the result must actually be a valid matching.
        assert len({a for a, _ in found}) == len(found)
        assert len({b for _, b in found}) == len(found)
        assert all(pair in edges for pair in found)


def test_perfect_matching_is_found():
    edges = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 2)]
    assert len(bipartite_matching(3, 3, edges)) == 3


def test_greedy_matching_can_be_beaten():
    """Where the obvious approach quietly returns a smaller answer.

    Worker 0 can do either job. Worker 1 can only do job 0. Greedy takes
    (0, 0) first, leaving worker 1 with nothing - one pairing. The maximum is
    two: give job 1 to worker 0 and job 0 to worker 1.
    """
    edges = [(0, 0), (0, 1), (1, 0)]
    greedy = greedy_matching(2, 2, edges)
    optimal = bipartite_matching(2, 2, edges)
    assert len(greedy) == 1
    assert len(optimal) == 2
    assert sorted(optimal) == [(0, 1), (1, 0)]


def test_matching_rejects_out_of_range_edges():
    with pytest.raises(ValueError):
        bipartite_matching(2, 2, [(5, 0)])


# ---------------------------------------------------------------------------
# project selection: min cut solving something that does not look like flow
# ---------------------------------------------------------------------------


def test_project_selection_picks_the_profitable_set():
    profits = {"alpha": 100, "beta": 200, "gamma": 50}
    costs = {"server": 200, "licence": 30}
    requires = {"alpha": ["server"], "beta": ["server"], "gamma": ["licence"]}

    profit, chosen = max_profit_projects(profits, costs, requires)
    # alpha + beta = 300 share one 200 server -> worth 100.
    # gamma = 50 needs a 30 licence -> worth 20. Total 120.
    assert profit == 120
    assert chosen == ["alpha", "beta", "gamma"]


def test_project_selection_declines_a_loss_making_project():
    profits = {"alpha": 10}
    costs = {"server": 500}
    requires = {"alpha": ["server"]}
    profit, chosen = max_profit_projects(profits, costs, requires)
    assert profit == 0
    assert chosen == []


# ---------------------------------------------------------------------------
# scale
# ---------------------------------------------------------------------------


@pytest.mark.perf
def test_dinic_beats_edmonds_karp_on_a_layered_graph():
    """Dinic saturates a whole level graph per phase; Edmonds-Karp does one
    path per BFS. On a wide layered network that is the difference between a
    handful of phases and thousands of individual augmentations.
    """
    width, layers = 24, 6
    edges = []
    node = 1
    previous = [0]
    for _ in range(layers):
        current = list(range(node, node + width))
        node += width
        for a in previous:
            for b in current:
                edges.append((a, b, 3))
        previous = current
    sink = node
    for a in previous:
        edges.append((a, sink, 3))

    start = time.perf_counter()
    ek = edmonds_karp(build(sink + 1, edges), 0, sink)
    ek_seconds = time.perf_counter() - start

    start = time.perf_counter()
    dn = dinic(build(sink + 1, edges), 0, sink)
    dinic_seconds = time.perf_counter() - start

    assert ek == dn, "both must still be correct"
    assert dinic_seconds < ek_seconds, (
        f"Dinic {dinic_seconds * 1000:.1f} ms vs "
        f"Edmonds-Karp {ek_seconds * 1000:.1f} ms")
