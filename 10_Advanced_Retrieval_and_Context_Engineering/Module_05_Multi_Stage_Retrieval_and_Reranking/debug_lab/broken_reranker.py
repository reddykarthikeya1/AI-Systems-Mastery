# Debug Lab: Cross-Encoder Reranker Sorts Worst Matches First
# Course 10 - Module 05 Multi-Stage Retrieval and Reranking

QUERY = "return policy for defective items"

# Candidates already retrieved by stage 1 (a fast bi-encoder / BM25 pass).
# Each is a short passage the reranker will re-score with a slower,
# higher-quality cross-encoder before the final list goes to the user.
CANDIDATES = [
    ("doc_1", "Defective items can be returned for a full refund within 30 days."),
    ("doc_2", "Our store hours are 9am to 9pm on weekdays."),
    ("doc_3", "Broken or defective products qualify for free return shipping."),
    ("doc_4", "We offer gift wrapping for an additional two dollars."),
]


def word_overlap_distance(query, passage):
    """Stand-in for a cross-encoder's raw output: a DISTANCE, where smaller
    means more relevant (0.0 = perfect match)."""
    q_words = set(query.lower().split())
    p_words = set(passage.lower().split())
    overlap = len(q_words & p_words)
    return 1.0 / (1.0 + overlap)  # more shared words -> smaller distance


def distance_to_similarity(distance):
    # The cross-encoder stage converts distance into a similarity score so
    # downstream consumers can treat "higher = more relevant" consistently.
    return 1.0 / (1.0 + distance)


def rerank(query, candidates):
    scored = []
    for doc_id, passage in candidates:
        distance = word_overlap_distance(query, passage)
        similarity = distance_to_similarity(distance)
        scored.append((doc_id, passage, similarity))
    scored.sort(key=lambda item: item[2])  # sort by the cross-encoder score
    return scored


if __name__ == "__main__":
    reranked = rerank(QUERY, CANDIDATES)

    print(f"Query: {QUERY!r}")
    print("Candidates with their cross-encoder similarity scores (higher = more relevant):")
    for doc_id, passage, sim in reranked:
        print(f"  {doc_id}: sim={sim:.4f}  {passage!r}")

    print(f"\nExpected: the reranked list should lead with the MOST relevant "
          f"passage (highest similarity) about defective-item returns.")
    print(f"Actual #1 result after reranking: {reranked[0][0]} -> {reranked[0][1]!r}")
