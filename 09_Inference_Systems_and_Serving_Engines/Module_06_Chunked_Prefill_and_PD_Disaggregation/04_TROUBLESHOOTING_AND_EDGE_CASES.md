# Module 06: Troubleshooting & Edge Cases

## 1. Top Production Failure Modes in Chunked Prefill

### Bug 1: Attention Mask Indexing Off-by-One Across Chunks
- **Symptom**: Model perplexity degrades on prompt tokens when chunking is enabled; generation hallucinates early tokens.
- **Root Cause**: When chunk $k$ attends to cached keys from chunks $1 \dots k-1$, failure to offset query position indices causes positional embedding distortion (RoPE frequency misalignment).
- **Fix**: Verify query position offsets: $\text{pos}_q = \text{offset}_{\text{chunk}} + i$.
