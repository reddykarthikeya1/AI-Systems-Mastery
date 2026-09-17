"""Reference Solution — Problem 01: Entity Relation Subgraph Extract

Topic: 07 Microsoft GraphRAG and Knowledge Graphs
"""

from __future__ import annotations


def entity_relation_subgraph_extract(triplets: list[tuple[str, str, str]], seed_entity: str) -> list[tuple[str, str, str]]:
    matched = [t for t in triplets if t[0] == seed_entity or t[2] == seed_entity]
    matched.sort()
    return matched
