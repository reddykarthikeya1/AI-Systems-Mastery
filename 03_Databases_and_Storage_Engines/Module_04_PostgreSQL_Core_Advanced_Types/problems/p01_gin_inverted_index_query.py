"""Problem 01 — Gin Inverted Index Query

Topic: 04 PostgreSQL Core Advanced Types
Target: Production-grade implementation

Query an inverted index of tag lists for documents containing all search terms.

Example:
    >>> idx = {"postgres": {1, 2, 3}, "acid": {2, 3, 4}, "jsonb": {1, 3}}
    >>> gin_inverted_index_query(idx, ["postgres", "acid"])
    {2, 3}

Hints:
    Hint 1: "Contains ALL search terms" means a document must survive being
        checked against every term in turn — this is an AND across terms,
        not an OR, so the candidate set can only shrink as you go.
    Hint 2: Start from the posting set of the first term and repeatedly
        intersect it with the posting set of each remaining term (a plain
        set().intersection_update loop over index.get(term, set())).
    Hint 3: A term missing from the index has an empty posting list, which
        should collapse the whole result to the empty set (not raise a
        KeyError), and an empty search_terms list must short-circuit to
        set() rather than falling through to "no terms filtered anything."
"""

from __future__ import annotations


def gin_inverted_index_query(index: dict[str, set[int]], search_terms: list[str]) -> set[int]:
    """Return document IDs that contain ALL search terms using inverted index.
    If search_terms is empty, return empty set.
    """
    raise NotImplementedError("Implement gin_inverted_index_query")
