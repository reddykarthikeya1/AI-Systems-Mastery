"""Problem 01 — Entity Relation Subgraph Extract

Topic: 07 Microsoft GraphRAG and Knowledge Graphs
Target: Production-grade implementation

Extract 1-hop knowledge graph neighborhood given seed entity.

Example:
    >>> entity_relation_subgraph_extract([("Python", "designed_by", "Guido"), ("Guido", "worked_at", "Google"), ("Java", "designed_by", "Gosling")], "Guido")
    [('Guido', 'worked_at', 'Google'), ('Python', 'designed_by', 'Guido')]

Hints:
    Hint 1: A "1-hop neighborhood" means the seed entity can sit on EITHER
        end of a relation — as the subject or as the object — not just one
        side.
    Hint 2: Filter with a comprehension checking `t[0] == seed_entity or
        t[2] == seed_entity`, then sort the matches directly with
        `list.sort()` and no key.
    Hint 3: Plain tuple sorting (no key) is what gives the required
        (subject, predicate, object) lexicographic order for free — don't
        sort by only one field — and a seed entity that appears nowhere
        must return an empty list rather than erroring.
"""

from __future__ import annotations


def entity_relation_subgraph_extract(triplets: list[tuple[str, str, str]], seed_entity: str) -> list[tuple[str, str, str]]:
    """triplets: list of (subject, predicate, object).
    Return all triplets where subject == seed_entity or object == seed_entity.
    Sorted alphabetically by (subject, predicate, object).
    """
    raise NotImplementedError("Implement entity_relation_subgraph_extract")
