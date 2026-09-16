"""Unit tests for DiskANN Vamana Graph Indexer."""

from __future__ import annotations

from diskann_vamana_sim import VamanaGraphIndexer


def test_vamana_out_degree_bounding():
    indexer = VamanaGraphIndexer(max_out_degree=3, alpha=1.2)
    indexer.insert("n1", [0.0, 0.0])
    indexer.insert("n2", [1.0, 0.0])
    indexer.insert("n3", [2.0, 0.0])
    indexer.insert("n4", [3.0, 0.0])
    indexer.insert("n5", [4.0, 0.0])
    indexer.insert("n6", [10.0, 10.0])

    indexer.build_index()

    for node, neighbors in indexer.graph.items():
        assert len(neighbors) <= 3


def test_vamana_alpha_pruning_keeps_diverse_shortcuts():
    indexer = VamanaGraphIndexer(max_out_degree=2, alpha=1.1)
    indexer.insert("origin", [0.0, 0.0])
    indexer.insert("close_1", [0.1, 0.0])
    indexer.insert("close_2", [0.12, 0.0])
    indexer.insert("far_corner", [0.0, 5.0])

    pruned = indexer.robust_prune(["close_1", "close_2", "far_corner"], "origin")
    assert "close_1" in pruned
    assert "far_corner" in pruned
