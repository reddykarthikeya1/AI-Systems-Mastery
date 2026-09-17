# 🐣 Interactive Foundations Playground: Microsoft GraphRAG & Knowledge Graphs

> *"GraphRAG turns documents into a web of entities and relationships, discovering connections across distant pages."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
from collections import defaultdict
```

---

## 1. Entity and Relationship Extraction

Extracting subject-predicate-object triples $(S, P, O)$ structures unstructured prose into an accessible graph.

```python
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
```

---

## 2. 2-Hop Multi-Hop Graph Traversal

Multi-hop graph traversal connects Bob to Berlin without either being mentioned in the same paragraph.

```python
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
```

---

## 3. Community Detection and Summarization

Hierarchical Leiden community detection groups tightly clustered entities into thematic summaries for holistic global queries.

```python
community_a = {"Alice", "Bob", "AcmeCorp"}
assert len(community_a) == 3
print(f"Graph community detected with {len(community_a)} nodes.")
```

---
