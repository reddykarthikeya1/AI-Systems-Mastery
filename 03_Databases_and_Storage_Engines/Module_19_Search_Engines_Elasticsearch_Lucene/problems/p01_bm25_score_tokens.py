"""Problem 01 — Bm25 Score Tokens

Topic: 19 Search Engines Elasticsearch Lucene
Target: Production-grade implementation

Calculate BM25 relevance score for document against query terms.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def bm25_score_tokens(query_terms: list[str], doc_tokens: list[str], avg_doc_len: float, doc_freqs: dict[str, int], total_docs: int, k1: float = 1.2, b: float = 0.75) -> float:
    """Calculate BM25 score:
    IDF = ln((total_docs - doc_freq + 0.5) / (doc_freq + 0.5) + 1.0)
    term_score = IDF * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avg_doc_len)))
    Returns sum of term scores for matched terms.
    """
    raise NotImplementedError("Implement bm25_score_tokens")
