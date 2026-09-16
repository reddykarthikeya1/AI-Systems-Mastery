from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class HybridSearchResult:
    doc_id: str
    rrf_score: float
    dense_rank: int | None
    sparse_rank: int | None


class HybridSearchRRFEngine:
    """Simulates Reciprocal Rank Fusion (RRF) over Dense and Sparse retrieval candidate lists."""

    def __init__(self, k: int = 60):
        self.k = k

    def fuse_rankings(
        self,
        dense_results: list[str],
        sparse_results: list[str],
        top_n: int = 5,
    ) -> list[HybridSearchResult]:
        rrf_scores: dict[str, float] = {}
        dense_ranks: dict[str, int] = {}
        sparse_ranks: dict[str, int] = {}

        # Process dense rankings (1-based index)
        for rank_idx, doc_id in enumerate(dense_results, start=1):
            dense_ranks[doc_id] = rank_idx
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (self.k + rank_idx))

        # Process sparse rankings
        for rank_idx, doc_id in enumerate(sparse_results, start=1):
            sparse_ranks[doc_id] = rank_idx
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (self.k + rank_idx))

        # Sort descending by RRF score
        sorted_docs = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)

        results = []
        for doc_id, score in sorted_docs[:top_n]:
            results.append(
                HybridSearchResult(
                    doc_id=doc_id,
                    rrf_score=round(score, 6),
                    dense_rank=dense_ranks.get(doc_id),
                    sparse_rank=sparse_ranks.get(doc_id),
                )
            )

        return results
