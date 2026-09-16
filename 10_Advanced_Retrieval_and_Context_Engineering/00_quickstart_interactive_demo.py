"""Course 10 Quickstart: Interactive Advanced Retrieval & DiskANN Vamana Demo."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "Module_03_Vector_Database_Internals" / "project_solution"))
from diskann_vamana_sim import VamanaGraphIndexer


def run_demo() -> None:
    print("=" * 70)
    print(" COURSE 10: ADVANCED RETRIEVAL & CONTEXT ENGINEERING QUICKSTART")
    print("=" * 70)

    print("\n[1] Microsoft DiskANN Vamana Graph Indexer with Alpha-Pruning:")
    indexer = VamanaGraphIndexer(max_out_degree=3, alpha=1.2)

    # Insert 6 vector nodes
    nodes = {
        "doc_gpu_h100": [1.0, 0.9, 0.0],
        "doc_gpu_b200": [1.1, 0.95, 0.05],
        "doc_nvlink":   [0.9, 0.8, 0.1],
        "doc_sql_mvcc": [0.0, 0.1, 0.95],
        "doc_sql_acid": [0.05, 0.15, 0.90],
        "doc_b_tree":   [0.1, 0.2, 0.85],
    }
    for nid, vec in nodes.items():
        indexer.insert(nid, vec)

    indexer.build_index()

    print("     * Built Vamana Graph Index with Max Out-Degree = 3, Alpha = 1.2:")
    for node, neighbors in indexer.graph.items():
        print(f"       -> Node '{node}' is connected to: {sorted(list(neighbors))}")

    print("\n" + "=" * 70)
    print(" QUICKSTART DEMO COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
