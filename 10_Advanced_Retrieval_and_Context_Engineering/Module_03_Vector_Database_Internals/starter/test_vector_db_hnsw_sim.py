from __future__ import annotations

import numpy as np
from vector_db_hnsw_sim import SimpleHNSWIndex


def test_hnsw_insertion_and_search():
    np.random.seed(42)
    dim = 8
    index = SimpleHNSWIndex(dim=dim, max_connections=3)

    # Insert 10 vectors
    for i in range(10):
        v = np.random.randn(dim).astype(np.float32)
        # Mark node 0 and node 5 as highway nodes
        index.insert(node_id=i, vec=v, is_highway=(i in [0, 5]))

    # Query identical to node 3
    query = index.vectors[3].copy()
    results = index.search_knn(query, k=1)

    assert len(results) > 0
    # Top-1 hit should be node 3 with similarity near 1.0
    assert results[0][0] == 3
    assert results[0][1] > 0.99
