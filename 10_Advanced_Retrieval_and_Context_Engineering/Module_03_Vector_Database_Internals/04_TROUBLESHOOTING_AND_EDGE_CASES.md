# Module 03: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Vector Databases

### Bug 1: Recall Collapse Under Filtered Vector Search
- **Symptom**: Query with metadata filter `{"category": "legal"}` returns only 1 result, even though 10,000 legal documents exist in the database.
- **Root Cause**: Post-filtering ANN search. The HNSW index traverses the top-10 nearest neighbors in vector space, and then discards 9 of them because they fail the metadata filter!
- **Fix**: Use single-stage filtered graph traversal (e.g. Qdrant / pgvector) where filtering bitsets restrict the neighbor traversal candidates during graph traversal.
