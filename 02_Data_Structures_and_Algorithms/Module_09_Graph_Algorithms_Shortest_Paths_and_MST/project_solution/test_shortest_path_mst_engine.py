"""Unit tests for ShortestPathMSTEngine."""
import pytest
from shortest_path_mst_engine import ShortestPathMSTEngine


def test_dijkstra():
    engine = ShortestPathMSTEngine[str]()
    engine.add_edge("A", "B", 4, directed=True)
    engine.add_edge("A", "C", 2, directed=True)
    engine.add_edge("C", "B", 1, directed=True)
    engine.add_edge("B", "D", 5, directed=True)
    engine.add_edge("C", "D", 8, directed=True)

    dist = engine.dijkstra("A")
    assert dist["A"] == 0
    assert dist["C"] == 2
    assert dist["B"] == 3  # Via C (2 + 1)
    assert dist["D"] == 8  # Via B (3 + 5)

def test_bellman_ford_and_negative_cycle():
    engine = ShortestPathMSTEngine[str]()
    engine.add_edge("A", "B", 4, directed=True)
    engine.add_edge("A", "C", 5, directed=True)
    engine.add_edge("B", "C", -2, directed=True)

    dist = engine.bellman_ford("A")
    assert dist["C"] == 2  # 4 + (-2)

    # Add negative cycle
    engine.add_edge("C", "A", -5, directed=True)
    with pytest.raises(ValueError, match="negative weight cycle"):
        engine.bellman_ford("A")

def test_kruskal_mst():
    engine = ShortestPathMSTEngine[int]()
    # Undirected weighted graph
    engine.add_edge(1, 2, 1, directed=False)
    engine.add_edge(2, 3, 2, directed=False)
    engine.add_edge(1, 3, 3, directed=False)
    engine.add_edge(3, 4, 4, directed=False)

    total_weight, mst_edges = engine.kruskal_mst()
    assert total_weight == 7.0  # 1 + 2 + 4
    assert len(mst_edges) == 3

def test_dijkstra_unreachable_node():
    engine = ShortestPathMSTEngine[str]()
    engine.add_edge("A", "B", 1, directed=True)
    engine.add_edge("C", "D", 2, directed=True)
    dist = engine.dijkstra("A")
    assert dist["B"] == 1
    assert dist["C"] == float("inf")
    assert dist["D"] == float("inf")

def test_kruskal_empty_and_disconnected():
    engine = ShortestPathMSTEngine[int]()
    weight, edges = engine.kruskal_mst()
    assert weight == 0.0
    assert edges == []
