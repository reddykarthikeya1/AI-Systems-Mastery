from __future__ import annotations

from graphrag_engine import SimpleGraphRAGEngine


def test_graphrag_community_detection_and_global_search():
    engine = SimpleGraphRAGEngine()

    # Add Cluster 1: Tech Hardware
    engine.add_entity("Apple", "Company", "Technology company")
    engine.add_entity("TSMC", "Company", "Semiconductor foundry")
    engine.add_relationship("Apple", "TSMC", "contracts chips from")

    # Add Cluster 2: Automotive
    engine.add_entity("Tesla", "Company", "EV manufacturer")
    engine.add_entity("Panasonic", "Company", "Battery supplier")
    engine.add_relationship("Tesla", "Panasonic", "purchases batteries from")

    reports = engine.build_communities_and_reports()
    assert len(reports) == 2

    # Global search must synthesize both community reports
    summary = engine.global_search("Summarize all corporate supply chains")
    assert "Apple" in summary
    assert "Tesla" in summary
