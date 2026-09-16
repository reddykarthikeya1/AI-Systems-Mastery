from __future__ import annotations

import numpy as np


class SimpleHNSWIndex:
    def __init__(self, dim: int, max_connections: int = 4):
        raise NotImplementedError("Implement SimpleHNSWIndex")

    def insert(self, node_id: int, vec: np.ndarray, is_highway: bool = False) -> None:
        raise NotImplementedError("Implement insert")

    def search_knn(self, query_vec: np.ndarray, k: int = 3) -> list[tuple[int, float]]:
        raise NotImplementedError("Implement search_knn")
