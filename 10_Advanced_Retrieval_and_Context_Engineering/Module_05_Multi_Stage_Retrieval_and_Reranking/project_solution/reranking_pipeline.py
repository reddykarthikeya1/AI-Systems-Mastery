from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class RerankedCandidate:
    doc_id: str
    text: str
    stage1_rank: int
    rerank_score: float


class TwoStageRetrievalPipeline:
    """Simulates Two-Stage Retrieval: Candidate filtering + Cross-attention scoring."""

    @staticmethod
    def simulate_cross_attention_score(query: str, text: str) -> float:
        """Simulates fine-grained cross-token token alignment score."""
        q_words = set(query.lower().split())
        t_words = text.lower().split()
        if not t_words or not q_words:
            return 0.0

        # Exact match count + phrase density
        exact_matches = sum(1 for w in t_words if w in q_words)
        match_ratio = exact_matches / max(len(q_words), 1)

        # Base score normalized in [0, 1]
        score = min(1.0, 0.2 + (match_ratio * 0.8))
        return round(score, 4)

    def rerank(
        self,
        query: str,
        candidates: list[dict[str, str]],
        top_k: int = 3,
    ) -> list[RerankedCandidate]:
        scored = []
        for idx, item in enumerate(candidates, start=1):
            score = self.simulate_cross_attention_score(query, item["text"])
            scored.append(
                RerankedCandidate(
                    doc_id=item["doc_id"],
                    text=item["text"],
                    stage1_rank=idx,
                    rerank_score=score,
                )
            )

        # Sort descending by cross-encoder score
        scored.sort(key=lambda c: c.rerank_score, reverse=True)
        return scored[:top_k]
