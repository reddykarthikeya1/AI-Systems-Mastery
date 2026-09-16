# Module 02: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Contextual Retrieval

### Bug 1: Context Header Diluting Chunk Specificity
- **Symptom**: Search queries for niche numerical values retrieve generic company overviews instead of specific calculation clauses.
- **Root Cause**: If contextual prefix $p_i$ is too long (e.g. 200 words), its embedding vector dominates the 50-word chunk, overshadowing local facts.
- **Fix**: Cap context prefix to $\le 40$ words ($< 20\%$ of total chunk size).
