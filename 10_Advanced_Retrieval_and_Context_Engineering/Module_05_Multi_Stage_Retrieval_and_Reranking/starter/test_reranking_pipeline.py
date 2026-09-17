from __future__ import annotations

from reranking_pipeline import TwoStageRetrievalPipeline


def test_two_stage_reranking_reordering():
    pipeline = TwoStageRetrievalPipeline()
    query = "python memory leaks profiling"

    # Candidate 1 was rank 1 in Stage 1 but is generic
    # Candidate 2 was rank 2 in Stage 1 but has exact query alignment
    candidates = [
        {"doc_id": "doc_1", "text": "Python is a popular programming language."},
        {"doc_id": "doc_2", "text": "Detecting python memory leaks with profiling tools."},
    ]

    reranked = pipeline.rerank(query, candidates, top_k=2)

    # doc_2 must be promoted to rank 1
    assert reranked[0].doc_id == "doc_2"
    assert reranked[0].stage1_rank == 2
    assert reranked[0].rerank_score > reranked[1].rerank_score
