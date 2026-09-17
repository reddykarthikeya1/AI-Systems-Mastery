"""Reference Solution — Problem 01: Gin Inverted Index Query

Topic: 04 PostgreSQL Core Advanced Types
"""

from __future__ import annotations


def gin_inverted_index_query(index: dict[str, set[int]], search_terms: list[str]) -> set[int]:
    if not search_terms:
        return set()
    result = None
    for term in search_terms:
        docs = index.get(term, set())
        if result is None:
            result = set(docs)
        else:
            result.intersection_update(docs)
        if not result:
            break
    return result if result is not None else set()
