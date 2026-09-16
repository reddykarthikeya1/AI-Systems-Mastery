"""Unit tests for DAGAndTraversalEngine."""
import pytest
from dag_and_traversal_engine import GraphEngine


def test_bfs_dfs_undirected():
    g = GraphEngine[str](directed=False)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "E")

    bfs_order = g.bfs("A")
    assert bfs_order[0] == "A"
    assert set(bfs_order) == {"A", "B", "C", "D", "E"}

    dfs_order = g.dfs("A")
    assert dfs_order[0] == "A"
    assert set(dfs_order) == {"A", "B", "C", "D", "E"}

def test_kahn_topological_sort_dag():
    dag = GraphEngine[int](directed=True)
    # 5 -> 2, 5 -> 0, 4 -> 0, 4 -> 1, 2 -> 3, 3 -> 1
    dag.add_edge(5, 2)
    dag.add_edge(5, 0)
    dag.add_edge(4, 0)
    dag.add_edge(4, 1)
    dag.add_edge(2, 3)
    dag.add_edge(3, 1)

    order = dag.topological_sort()
    assert len(order) == 6
    # Verify relative ordering
    pos = {node: i for i, node in enumerate(order)}
    assert pos[5] < pos[2] < pos[3] < pos[1]
    assert pos[4] < pos[0]

def test_topological_sort_cycle_detection():
    cyclic = GraphEngine[int](directed=True)
    cyclic.add_edge(1, 2)
    cyclic.add_edge(2, 3)
    cyclic.add_edge(3, 1)

    with pytest.raises(ValueError, match="Cycle detected"):
        cyclic.topological_sort()

def test_bfs_dfs_empty_and_isolated():
    g = GraphEngine[str](directed=True)
    assert g.bfs("Z") == []
    assert g.dfs("Z") == []
    g.add_vertex("Solo")
    assert g.bfs("Solo") == ["Solo"]
    assert g.dfs("Solo") == ["Solo"]

def test_disconnected_graph_components():
    g = GraphEngine[int](directed=False)
    g.add_edge(1, 2)
    g.add_edge(3, 4)
    g.add_vertex(5)
    assert g.count_connected_components() == 3

def test_topological_sort_undirected_error():
    undirected = GraphEngine[int](directed=False)
    undirected.add_edge(1, 2)
    with pytest.raises(ValueError, match="directed graph"):
        undirected.topological_sort()
