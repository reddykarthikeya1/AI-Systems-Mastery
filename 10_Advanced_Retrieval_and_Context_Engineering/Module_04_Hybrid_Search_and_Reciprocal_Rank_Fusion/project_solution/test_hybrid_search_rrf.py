from __future__ import annotations

from hybrid_search_rrf import HybridSearchRRFEngine


def test_rrf_scoring_and_fusion():
    engine = HybridSearchRRFEngine(k=60)

    # doc_A is rank 1 in both -> 1/61 + 1/61 = 2/61 = ~0.032786
    # doc_B is rank 2 in dense, absent in sparse -> 1/62 = ~0.016129
    # doc_C is rank 1 in sparse, absent in dense -> 1/61 = ~0.016393
    dense_hits = ["doc_A", "doc_B"]
    sparse_hits = ["doc_C", "doc_A"]

    fused = engine.fuse_rankings(dense_hits, sparse_hits, top_n=3)

    assert len(fused) == 3
    # doc_A has 1/61 + 1/62 = ~0.032524
    assert fused[0].doc_id == "doc_A"
    expected_a = (1.0 / 61.0) + (1.0 / 62.0)
    assert abs(fused[0].rrf_score - expected_a) < 1e-4

    # doc_C (rank 1 sparse) must beat doc_B (rank 2 dense)
    assert fused[1].doc_id == "doc_C"
    assert fused[2].doc_id == "doc_B"
