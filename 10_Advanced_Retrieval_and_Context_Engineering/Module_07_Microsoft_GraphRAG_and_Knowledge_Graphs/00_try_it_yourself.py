"""Beginner playground for Module 07 - Microsoft GraphRAG & Knowledge Graphs.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from collections import defaultdict

# -------------------------------------------- 1. Entity and Relationship Extraction
triples = [
    ("Alice", "located_in", "Berlin"),
    ("AcmeCorp", "industry", "Tech"),
    ("Bob", "collaborates_with", "Alice")
]

graph = defaultdict(list)
for s, p, o in triples:
    graph[s].append((p, o))

assert len(graph["Alice"]) == 1
assert ("located_in", "Berlin") in graph["Alice"]
print(f"Extracted knowledge graph edges for Alice: {graph['Alice']}")

# -------------------------------------------- 2. 2-Hop Multi-Hop Graph Traversal
# Where is Bob's collaborator located?
def two_hop(start):
    cities = []
    for p1, o1 in graph.get(start, []):
        for p2, o2 in graph.get(o1, []):
            if p2 == "located_in":
                cities.append(o2)
    return cities

bob_connected_cities = two_hop("Bob")
assert bob_connected_cities == ["Berlin"]
print(f"Multi-hop GraphRAG connected Bob -> Berlin: {bob_connected_cities}")

# -------------------------------------------- 3. Community Detection and Summarization
community_a = {"Alice", "Bob", "AcmeCorp"}
assert len(community_a) == 3
print(f"Graph community detected with {len(community_a)} nodes.")

print()
print("All checks passed.")
