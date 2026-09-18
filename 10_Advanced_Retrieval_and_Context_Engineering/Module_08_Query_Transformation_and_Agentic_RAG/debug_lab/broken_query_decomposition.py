# Debug Lab: Agentic RAG Sub-Query Results Overwrite Each Other
# Course 10 - Module 08 Query Transformation and Agentic RAG

# Simulated retriever: a fixed lookup table of what each sub-question
# retrieves, standing in for an embedding search over a document store.
RETRIEVER_RESULTS = {
    "What is the refund window?": [("doc_refund", 0.91), ("doc_faq", 0.40)],
    "Do exchanges need a receipt?": [("doc_exchange", 0.88), ("doc_faq", 0.35)],
    "How long does shipping take?": [("doc_shipping", 0.85), ("doc_faq", 0.30)],
}


def decompose_query(complex_query):
    """An agentic RAG planner breaks a multi-part question into independent
    sub-questions that can each be retrieved and answered separately."""
    return list(RETRIEVER_RESULTS.keys())


def retrieve(sub_query):
    return RETRIEVER_RESULTS[sub_query]


def gather_context(complex_query):
    """Run every sub-question through the retriever and merge all retrieved
    documents into one combined context for the final answer synthesis
    step. Every distinct document retrieved by any sub-question should
    survive into the merged context."""
    sub_queries = decompose_query(complex_query)
    combined = {}
    for sub_query in sub_queries:
        results = retrieve(sub_query)
        for rank, (doc_id, score) in enumerate(results):
            combined[rank] = (doc_id, score)
    return combined


if __name__ == "__main__":
    complex_query = ("What's the refund window, do exchanges need a receipt, "
                      "and how long does shipping take?")

    sub_queries = decompose_query(complex_query)
    combined_context = gather_context(complex_query)

    print(f"Complex query decomposed into {len(sub_queries)} sub-questions:")
    for sq in sub_queries:
        print(f"  - {sq!r} -> {retrieve(sq)}")

    all_expected_docs = {doc_id for results in RETRIEVER_RESULTS.values() for doc_id, _ in results}
    surviving_docs = {doc_id for doc_id, _ in combined_context.values()}

    print(f"\nExpected: all {len(all_expected_docs)} distinct documents retrieved "
          f"across the 3 sub-questions should be in the merged context: "
          f"{sorted(all_expected_docs)}")
    print(f"Actual merged context: {combined_context}")
    print(f"Actual surviving documents ({len(surviving_docs)}): {sorted(surviving_docs)}")
