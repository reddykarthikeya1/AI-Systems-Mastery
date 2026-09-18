# Debug Lab: GraphRAG Entity Ranking Ignores Incoming Relationships
# Course 10 - Module 07 Microsoft GraphRAG and Knowledge Graphs

# (source_entity, target_entity, relation) triples extracted from documents,
# the way GraphRAG builds its knowledge graph before community detection.
RELATIONSHIPS = [
    ("Alice", "Acme Corp", "works_at"),
    ("Bob", "Acme Corp", "works_at"),
    ("Carol", "Acme Corp", "works_at"),
    ("Alice", "Bob", "knows"),
]


def compute_degree_centrality(relationships):
    """Rank entities by how connected they are in the knowledge graph, so the
    most important (central) entities get prioritized when assembling
    context for a query. A relationship connects BOTH entities involved --
    "Alice works_at Acme Corp" makes Acme Corp just as connected as Alice."""
    degree = {}
    for source, target, relation in relationships:
        degree[source] = degree.get(source, 0) + 1
    return degree


def top_entities(degree, k=1):
    return sorted(degree, key=lambda e: degree[e], reverse=True)[:k]


if __name__ == "__main__":
    degree = compute_degree_centrality(RELATIONSHIPS)
    ranked = top_entities(degree, k=1)

    print("Relationships extracted from the source documents:")
    for s, t, r in RELATIONSHIPS:
        print(f"  {s} --{r}--> {t}")

    print(f"\nComputed degree centrality: {degree}")
    print("Expected: 'Acme Corp' is referenced by three separate relationships "
          "(it's the clear hub of this graph) and should be the #1 ranked entity.")
    print(f"Actual top-ranked entity for context building: {ranked[0]}")
    print(f"Is 'Acme Corp' even present in the degree scores? {'Acme Corp' in degree}")
