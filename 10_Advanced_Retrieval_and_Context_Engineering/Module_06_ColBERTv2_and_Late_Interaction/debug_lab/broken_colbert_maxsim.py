# Debug Lab: ColBERT Late Interaction Scoring Favors the Wrong Document
# Course 10 - Module 06 ColBERTv2 and Late Interaction

import math


def cosine_sim(u, v):
    dot = sum(a * b for a, b in zip(u, v))
    norm_u = math.sqrt(sum(a * a for a in u))
    norm_v = math.sqrt(sum(b * b for b in v))
    if norm_u == 0 or norm_v == 0:
        return 0.0
    return dot / (norm_u * norm_v)


def late_interaction_score(query_token_embs, doc_token_embs):
    """ColBERT's MaxSim operator: for EACH query token, find its single best
    matching document token (max cosine similarity), then sum those per-token
    maxes. This lets a document earn full credit for exactly matching one
    important query term, even if the rest of the document is unrelated."""
    total = 0.0
    for q_emb in query_token_embs:
        sims = [cosine_sim(q_emb, d_emb) for d_emb in doc_token_embs]
        total += sum(sims) / len(sims)
    return total


if __name__ == "__main__":
    # Query: "python exceptions" (2 token embeddings, toy 2D vectors).
    query_tokens = [(1.0, 0.0), (0.0, 1.0)]  # "python", "exceptions"

    # doc_A: one token is a NEAR-PERFECT match for "exceptions", the other
    # token is unrelated to either query term. This is the kind of document
    # late interaction is designed to reward.
    doc_a_tokens = [(0.05, 0.99), (-1.0, 0.02)]  # "exceptions"-like, then noise

    # doc_B: both tokens are mediocre, generic matches to both query terms --
    # never a strong match to anything, just vaguely on-topic everywhere.
    doc_b_tokens = [(0.5, 0.5), (0.45, 0.45)]

    score_a = late_interaction_score(query_tokens, doc_a_tokens)
    score_b = late_interaction_score(query_tokens, doc_b_tokens)

    print(f"Query tokens: {query_tokens}")
    print(f"doc_A tokens (one near-perfect match, one irrelevant): {doc_a_tokens}")
    print(f"doc_B tokens (uniformly mediocre matches): {doc_b_tokens}")
    print(f"\nExpected: MaxSim should reward doc_A's exact per-term match, so "
          f"score_a > score_b.")
    print(f"Actual score_a: {score_a:.4f}")
    print(f"Actual score_b: {score_b:.4f}")
    print(f"Actual winner: {'doc_A' if score_a > score_b else 'doc_B'}")
