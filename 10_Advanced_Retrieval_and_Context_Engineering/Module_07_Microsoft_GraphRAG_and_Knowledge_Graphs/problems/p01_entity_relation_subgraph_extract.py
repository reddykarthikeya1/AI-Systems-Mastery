"""Problem 01 — Entity Relation Subgraph Extract

Topic: 07 Microsoft GraphRAG and Knowledge Graphs
Target: Production-grade implementation

Extract 1-hop knowledge graph neighborhood given seed entity.

Hints:
    Hint 1: Review module invariants and algorithm specifications.
    Hint 2: Handle edge cases, empty sequences, and format constraints cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def entity_relation_subgraph_extract(triplets: list[tuple[str, str, str]], seed_entity: str) -> list[tuple[str, str, str]]:
    """triplets: list of (subject, predicate, object).
    Return all triplets where subject == seed_entity or object == seed_entity.
    Sorted alphabetically by (subject, predicate, object).
    """
    raise NotImplementedError("Implement entity_relation_subgraph_extract")
