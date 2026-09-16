from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class HybridSearchResult:
    doc_id: str
    rrf_score: float
    dense_rank: int | None
    sparse_rank: int | None


class HybridSearchRRFEngine:
    def __init__(self, k: int = 60):
        raise NotImplementedError("Implement HybridSearchRRFEngine")

    def fuse_rankings(
        self,
        dense_results: list[str],
        sparse_results: list[str],
        top_n: int = 5,
    ) -> list[HybridSearchResult]:
        raise NotImplementedError("Implement fuse_rankings")
