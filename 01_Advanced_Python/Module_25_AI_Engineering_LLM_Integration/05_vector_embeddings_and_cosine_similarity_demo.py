#!/usr/bin/env python3
"""Module 23: Vector Embeddings & Cosine Similarity Demonstration.

This script demonstrates vector search, embedding indexing, and cosine similarity ranking.
"""

from __future__ import annotations

import math


def cosine_sim(vec_a: list[float], vec_b: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vec_a, vec_b, strict=False))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class SimpleVectorStore:
    def __init__(self) -> None:
        self.documents: list[tuple[str, list[float]]] = []

    def add_document(self, text: str, embedding: list[float]) -> None:
        self.documents.append((text, embedding))

    def search(self, query_embedding: list[float], top_k: int = 2) -> list[tuple[str, float]]:
        scores = [(text, cosine_sim(query_embedding, emb)) for text, emb in self.documents]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


def main() -> None:
    print("=" * 60)
    print("  Vector Embeddings & Semantic Search Demonstration")
    print("=" * 60)

    store = SimpleVectorStore()
    store.add_document("FastAPI provides automatic OpenAPI docs.", [0.90, 0.20, 0.05])
    store.add_document("Python asyncio runs on an event loop.", [0.85, 0.40, 0.10])
    store.add_document("The quick brown fox jumps over the dog.", [0.10, 0.05, 0.90])

    query_vec = [0.88, 0.30, 0.08]  # Query about async web frameworks
    results = store.search(query_vec, top_k=2)

    print("Top Search Results for Query Vector:")
    for text, score in results:
        print(f"  - [Score: {score:.4f}] {text}")


if __name__ == "__main__":
    main()
