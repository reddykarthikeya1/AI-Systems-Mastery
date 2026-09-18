# Debug Lab Solution & Forensic Post-Mortem

## Incident: The Graph's Obvious Hub Entity Is Missing From Rankings

---

### Forensic Root Cause Analysis
`compute_degree_centrality()` only increments a score for the `source`
entity of each relationship triple:

```python
for source, target, relation in relationships:
    degree[source] = degree.get(source, 0) + 1
```

`target` is unpacked from the tuple but never used. Knowledge-graph
relationships like `"Alice works_at Acme Corp"` connect *both* entities --
the whole point of degree centrality is to measure how many relationships
touch an entity, regardless of which side of the triple it was written on.
By only counting `source`, any entity that is purely a *target* across all of
its relationships (like `Acme Corp`, which never initiates a relationship in
this dataset, only receives them) accumulates a degree of exactly zero and
never even gets a dictionary entry. Since GraphRAG uses this kind of ranking
to decide which entities' summaries make it into the limited context window
sent to the LLM, the most important hub entity in the entire graph is
silently excluded from every query that depends on this ranking.

---

### Production Corrective Action & Code Fix

```python
def compute_degree_centrality(relationships):
    degree = {}
    for source, target, relation in relationships:
        degree[source] = degree.get(source, 0) + 1
        degree[target] = degree.get(target, 0) + 1
    return degree
```

Incrementing both `source` and `target` for every relationship gives
`Acme Corp` a degree of 3 (from the three `works_at` relationships pointing
to it), correctly making it the top-ranked entity, ahead of `Alice`'s degree
of 2.

---

### Production Prevention Invariants
1. **Unused Unpacked Variables Are a Signal:** `target` being unpacked from
   the loop but never referenced in the body is exactly the kind of thing a
   linter or code reviewer should flag -- it's rarely intentional.
2. **Directed Extraction, Undirected Semantics Test:** When relationships are
   stored as directed triples but represent undirected "is connected to"
   semantics, test that both endpoints of a relationship show up in any
   derived connectivity metric.
3. **Known-Hub Fixture:** Build a small test graph with one deliberately
   heavily-referenced entity that never appears as a `source`, and assert it
   still ranks at or near the top of degree centrality -- this exact class of
   bug is invisible in graphs where every entity happens to appear on both
   sides of at least one relationship.
