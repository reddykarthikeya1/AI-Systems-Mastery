# Debug Lab: Contextual Retrieval Pairs Each Chunk With the Wrong Context
# Course 10 - Module 02 Contextual Retrieval Architecture

import math

CHUNKS = [
    "Refunds are issued within five business days of the return arriving at our warehouse.",
    "Exchanges require the original receipt and must happen within thirty days of purchase.",
    "Shipping to international addresses adds seven to ten business days to delivery time.",
]

# Simulates a cheap LLM call that writes a short situating sentence for each
# chunk before it gets embedded -- Anthropic's "contextual retrieval" recipe.
CHUNK_TOPICS = ["refund", "exchange", "shipping"]


def generate_context(chunk_index):
    topic = CHUNK_TOPICS[chunk_index]
    return f"This chunk explains the store's {topic} policy."


def contextualize_chunks(chunks):
    """Prepend each chunk's own situating context before embedding, so the
    embedding captures what the chunk is about even in isolation."""
    contexts = [generate_context(i) for i in range(len(chunks))]
    paired = list(zip(contexts[1:], chunks))
    return [f"{ctx} {chunk}" for ctx, chunk in paired]


def embed(text, vocab):
    text_lower = text.lower()
    return tuple(text_lower.count(word) for word in vocab)


def cosine_sim(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


if __name__ == "__main__":
    vocab = ["refund", "exchange", "shipping", "receipt", "warehouse", "international"]

    contextualized = contextualize_chunks(CHUNKS)
    chunk_embeddings = [embed(c, vocab) for c in contextualized]

    query = "How long does international shipping take?"
    query_embedding = embed(query, vocab)

    sims = [cosine_sim(query_embedding, emb) for emb in chunk_embeddings]
    best_idx = sims.index(max(sims))

    print(f"Source corpus has {len(CHUNKS)} chunks (refund, exchange, shipping).")
    print(f"Chunks that actually made it into the embedded index: {len(contextualized)}")
    for i, c in enumerate(contextualized):
        print(f"  embedded[{i}]: {c!r}")

    print(f"\nQuery: {query!r}")
    print("Expected: the top match should be the shipping-policy chunk "
          f"({CHUNKS[2][:40]!r}...).")
    print(f"Actual similarities over the embedded index: {[round(s, 3) for s in sims]}")
    print(f"Actual top match text: {contextualized[best_idx]!r}")
    print(f"Is the shipping chunk even present in the embedded index? "
          f"{CHUNKS[2] in contextualized}")
