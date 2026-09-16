# Module 04: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Hybrid Search

### Bug 1: Missing Document ID Mapping Invariant
- **Symptom**: Hybrid search returns duplicated documents with divergent ranks.
- **Root Cause**: BM25 index stores document integer IDs (`1042`), while vector DB stores UUID strings (`"doc_1042"`). RRF fails to match documents, splitting them into duplicate disjoint candidates.
- **Fix**: Enforce a strict canonical string ID schema across both retrieval backends prior to RRF aggregation.
