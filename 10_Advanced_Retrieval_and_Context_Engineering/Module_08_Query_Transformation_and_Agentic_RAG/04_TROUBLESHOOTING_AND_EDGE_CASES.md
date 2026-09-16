# Module 08: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Agentic RAG

### Bug 1: Infinite Query Rewrite Loops
- **Symptom**: Agentic RAG request times out after 120 seconds, executing 25 consecutive web searches.
- **Root Cause**: The evaluation agent rejects retrieved context because of impossible precision criteria, repeatedly rewriting queries.
- **Fix**: Enforce a strict recursion limit (max 3 retrieval attempts). If criteria are not met, degrade gracefully and answer with the best available context with an explicit uncertainty disclaimer.
