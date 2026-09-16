# Module 07: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in GraphRAG

### Bug 1: Entity Name Fragmentation
- **Symptom**: Knowledge graph contains disjoint nodes for `"Apple"`, `"Apple Inc."`, `"Apple Corporation"`, and `"AAPL"`, splitting community clusters.
- **Root Cause**: Missing entity resolution / coreference deduplication during graph ingestion.
- **Fix**: Apply an entity canonicalization step using embedding similarity and string normalization before inserting edges into the graph store.
