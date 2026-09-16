# Module 01: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Document Chunking

### Bug 1: Parent Node Orphan Leaks
- **Symptom**: Vector search returns top hits, but LLM receives empty context strings.
- **Root Cause**: When documents are re-indexed or deleted, child vectors are updated in the vector DB, but parent chunks in document storage (MongoDB/S3) are purged or desynchronized, leaving child vectors pointing to non-existent parent IDs.
- **Fix**: Use transactional atomic upserts and cascading deletes between vector index and parent document stores.
