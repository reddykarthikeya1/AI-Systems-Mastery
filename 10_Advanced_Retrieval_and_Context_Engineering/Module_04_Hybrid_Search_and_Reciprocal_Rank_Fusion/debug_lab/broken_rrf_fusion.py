# Debug Lab: Reciprocal Rank Fusion Silently Drops the Top-Ranked Hit
# Course 10 - Module 04 Hybrid Search and Reciprocal Rank Fusion

def reciprocal_rank_fusion(ranked_lists):
    """Combine several ranked result lists (e.g. BM25 keyword search and
    dense vector search) into one fused ranking. Each document's fused score
    is the sum of 1/rank across every list it appears in, rewarding
    documents that rank well across multiple retrievers."""
    scores = {}
    for ranked_list in ranked_lists:
        for rank, doc_id in enumerate(ranked_list):
            try:
                contribution = 1 / rank
            except ZeroDivisionError:
                continue  # this document's rank-0 contribution is skipped
            scores[doc_id] = scores.get(doc_id, 0.0) + contribution
    return scores


if __name__ == "__main__":
    bm25_results = ["doc_A", "doc_B", "doc_C", "doc_D"]
    vector_results = ["doc_A", "doc_C", "doc_E", "doc_B"]

    fused_scores = reciprocal_rank_fusion([bm25_results, vector_results])
    fused_ranking = sorted(fused_scores, key=lambda d: fused_scores[d], reverse=True)

    print(f"BM25 ranked list:   {bm25_results}")
    print(f"Vector ranked list: {vector_results}")
    print("doc_A is the #1 hit in BOTH retrievers -- the strongest possible "
          "signal a hybrid search system can get.")
    print(f"\nExpected: doc_A should have the HIGHEST fused score and lead the "
          f"final ranking.")
    print(f"Actual fused scores: { {k: round(v, 4) for k, v in fused_scores.items()} }")
    print(f"Actual fused ranking (best to worst): {fused_ranking}")
    print(f"Is doc_A present in the fused scores at all? {'doc_A' in fused_scores}")
