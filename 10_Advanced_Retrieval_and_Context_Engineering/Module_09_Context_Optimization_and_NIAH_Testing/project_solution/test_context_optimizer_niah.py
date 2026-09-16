from __future__ import annotations

from context_optimizer_niah import ContextOptimizerNIAH


def test_u_shaped_context_reordering():
    # 5 documents ranked from 1 (best) to 5 (worst)
    docs = ["doc_1", "doc_2", "doc_3", "doc_4", "doc_5"]
    reordered = ContextOptimizerNIAH.reorder_context_u_shaped(docs)

    # doc_1 (best) should be at the very end
    assert reordered[-1] == "doc_1"
    # doc_2 (second best) should be at the very start
    assert reordered[0] == "doc_2"


def test_synthetic_niah_insertion():
    needle = "SECRET_KEY_9988"
    _, res = ContextOptimizerNIAH.run_synthetic_niah(
        haystack_words=500,
        needle=needle,
        depth_percent=50.0,
    )
    assert res.needle_found is True
    assert res.needle_depth_percent == 50.0
