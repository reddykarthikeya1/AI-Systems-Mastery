"""Reference Solution — Problem 01: Bm25 Score Tokens

Topic: 19 Search Engines Elasticsearch Lucene
"""

from __future__ import annotations


def bm25_score_tokens(query_terms: list[str], doc_tokens: list[str], avg_doc_len: float, doc_freqs: dict[str, int], total_docs: int, k1: float = 1.2, b: float = 0.75) -> float:
    import math
    from collections import Counter
    counts = Counter(doc_tokens)
    doc_len = len(doc_tokens)
    score = 0.0
    for term in query_terms:
        if term not in counts:
            continue
        tf = counts[term]
        df = doc_freqs.get(term, 0)
        idf = math.log((total_docs - df + 0.5) / (df + 0.5) + 1.0)
        numerator = tf * (k1 + 1.0)
        denominator = tf + k1 * (1.0 - b + b * (doc_len / avg_doc_len if avg_doc_len > 0 else 1.0))
        score += idf * (numerator / denominator)
    return score
