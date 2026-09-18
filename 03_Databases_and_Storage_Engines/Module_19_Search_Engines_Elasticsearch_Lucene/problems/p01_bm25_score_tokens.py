"""Problem 01 — Bm25 Score Tokens

Topic: 19 Search Engines Elasticsearch Lucene
Target: Production-grade implementation

Calculate BM25 relevance score for document against query terms.

Example:
    >>> bm25_score_tokens(
    ...     query_terms=["database", "acid"],
    ...     doc_tokens=["database", "storage", "database", "acid", "engine"],
    ...     avg_doc_len=5.0,
    ...     doc_freqs={"database": 10, "acid": 5},
    ...     total_docs=100,
    ... )
    6.023022156659784

Hints:
    Hint 1: BM25 is a per-term score that gets summed — a query term that
        never occurs in this document contributes nothing at all, it isn't
        penalized or scored as zero-with-a-remainder.
    Hint 2: Use collections.Counter over doc_tokens to get each term's
        in-document term frequency (tf), then apply the given IDF and
        term_score formulas directly with math.log; total doc_len is just
        len(doc_tokens).
    Hint 3: Skip query terms with tf == 0 (not in counts) rather than
        plugging tf=0 into the formula, and guard the doc_len / avg_doc_len
        ratio against avg_doc_len == 0 (treat that ratio as 1.0) so a
        degenerate corpus average doesn't raise a ZeroDivisionError.
"""

from __future__ import annotations


def bm25_score_tokens(query_terms: list[str], doc_tokens: list[str], avg_doc_len: float, doc_freqs: dict[str, int], total_docs: int, k1: float = 1.2, b: float = 0.75) -> float:
    """Calculate BM25 score:
    IDF = ln((total_docs - doc_freq + 0.5) / (doc_freq + 0.5) + 1.0)
    term_score = IDF * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avg_doc_len)))
    Returns sum of term scores for matched terms.
    """
    raise NotImplementedError("Implement bm25_score_tokens")
