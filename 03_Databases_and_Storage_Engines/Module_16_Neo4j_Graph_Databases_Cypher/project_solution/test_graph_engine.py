"""Module 16 Test Suite: Neo4j & Graph Database Engine."""

from __future__ import annotations

from graph_engine import PropertyGraphEngine


def test_index_free_adjacency_pointer_linking() -> None:
    engine = PropertyGraphEngine()
    alice = engine.create_node("u1", ["User"], {"name": "Alice"})
    bob = engine.create_node("u2", ["User"], {"name": "Bob"})

    rel = engine.create_relationship("r1", "u1", "u2", "FOLLOWS", {"since": 2024})

    # Direct memory pointer checks (Index-Free Adjacency)
    assert len(alice.outgoing) == 1
    assert alice.outgoing[0] is rel
    assert alice.outgoing[0].end_node is bob

    assert len(bob.incoming) == 1
    assert bob.incoming[0] is rel
    assert bob.incoming[0].start_node is alice


def test_match_pattern_with_labels_and_properties() -> None:
    engine = PropertyGraphEngine()
    engine.create_node("u1", ["User"], {"name": "Alice"})
    engine.create_node("u2", ["User"], {"name": "Bob"})
    engine.create_node("acc1", ["Account"], {"currency": "USD"})
    engine.create_node("acc2", ["Account"], {"currency": "EUR"})

    engine.create_relationship("r1", "u1", "acc1", "OWNS")
    engine.create_relationship("r2", "u2", "acc2", "OWNS")
    engine.create_relationship("t1", "acc1", "acc2", "TRANSFERRED_TO", {"amount": 50000})

    # Pattern: (:Account)-[:TRANSFERRED_TO]->(:Account) where amount=50000
    results = engine.match_pattern(
        start_label="Account",
        rel_type="TRANSFERRED_TO",
        end_label="Account",
        where_props={"amount": 50000},
    )

    assert len(results) == 1
    src, rel, dest = results[0]
    assert src.node_id == "acc1"
    assert dest.node_id == "acc2"
    assert rel.properties["amount"] == 50000


def test_shortest_path_bfs() -> None:
    engine = PropertyGraphEngine()
    for nid in ["A", "B", "C", "D", "X"]:
        engine.create_node(nid, ["Node"], {})

    # Path 1: A -> B -> C -> D (3 hops)
    engine.create_relationship("e1", "A", "B", "CONNECTS")
    engine.create_relationship("e2", "B", "C", "CONNECTS")
    engine.create_relationship("e3", "C", "D", "CONNECTS")

    # Shortcut: A -> X -> D (2 hops)
    engine.create_relationship("e4", "A", "X", "CONNECTS")
    engine.create_relationship("e5", "X", "D", "CONNECTS")

    path = engine.shortest_path("A", "D")
    assert path == ["A", "X", "D"]


def test_circular_fraud_ring_detection() -> None:
    engine = PropertyGraphEngine()
    for i in range(1, 5):
        engine.create_node(f"acc_{i}", ["Account"], {})

    # Acc1 -> Acc2 -> Acc3 -> Acc4 -> Acc1 (Cycle of length 4)
    engine.create_relationship("t1", "acc_1", "acc_2", "TRANSFERRED")
    engine.create_relationship("t2", "acc_2", "acc_3", "TRANSFERRED")
    engine.create_relationship("t3", "acc_3", "acc_4", "TRANSFERRED")
    engine.create_relationship("t4", "acc_4", "acc_1", "TRANSFERRED")

    cycles = engine.find_cycles("acc_1", min_length=3, max_length=5)
    assert len(cycles) == 1
    assert cycles[0] == ["acc_1", "acc_2", "acc_3", "acc_4", "acc_1"]


def test_pagerank_centrality() -> None:
    engine = PropertyGraphEngine()
    # Star topology: 4 leaf nodes point to 1 central authority node
    engine.create_node("center", ["Server"], {})
    for i in range(1, 5):
        nid = f"leaf_{i}"
        engine.create_node(nid, ["Server"], {})
        engine.create_relationship(f"r_{i}", nid, "center", "ROUTES_TO")

    pr = engine.pagerank(damping=0.85, max_iterations=30)

    # Center node must have strictly higher PageRank than all leaves
    center_rank = pr["center"]
    for i in range(1, 5):
        assert center_rank > pr[f"leaf_{i}"]
