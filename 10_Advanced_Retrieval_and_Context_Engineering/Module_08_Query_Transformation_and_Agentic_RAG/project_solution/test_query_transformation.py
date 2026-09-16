from __future__ import annotations

from query_transformation import QueryTransformer


def test_query_decomposition():
    q = "Python async performance vs Go goroutines throughput"
    sub_queries = QueryTransformer.decompose_query(q)
    assert len(sub_queries) == 2
    assert "Python async" in sub_queries[0]
    assert "Go goroutines" in sub_queries[1]


def test_relevance_grading():
    query = "memory leak profiling"
    good_context = "This tutorial explains memory leak profiling using tracemalloc."
    bad_context = "This tutorial explains how to build web pages using CSS."

    assert QueryTransformer.grade_retrieval_relevance(query, good_context) is True
    assert QueryTransformer.grade_retrieval_relevance(query, bad_context) is False
