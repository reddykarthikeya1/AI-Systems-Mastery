"""Problem 01 — Gin Inverted Index Query

Topic: 04 PostgreSQL Core Advanced Types
Target: Production-grade implementation

Query an inverted index of tag lists for documents containing all search terms.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def gin_inverted_index_query(index: dict[str, set[int]], search_terms: list[str]) -> set[int]:
    """Return document IDs that contain ALL search terms using inverted index.
    If search_terms is empty, return empty set.
    """
    raise NotImplementedError("Implement gin_inverted_index_query")
