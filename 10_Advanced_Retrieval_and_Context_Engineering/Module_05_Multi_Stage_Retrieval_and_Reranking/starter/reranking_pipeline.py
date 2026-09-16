from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class RerankedCandidate:
    doc_id: str
    text: str
    stage1_rank: int
    rerank_score: float


class TwoStageRetrievalPipeline:
    def rerank(
        self,
        query: str,
        candidates: list[dict[str, str]],
        top_k: int = 3,
    ) -> list[RerankedCandidate]:
        raise NotImplementedError("Implement rerank")
