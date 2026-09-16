# Project Guide: Building a Multi-Tiered Agent Memory Manager

In this project, you will build an enterprise agent memory manager combining working memory buffering, episodic vector scoring, and reflection synthesis.

---

## Three-Tier Implementation Path

### Tier 1: Working Memory Buffer (Required)
- Implement sliding window conversation buffer bounded by max turns or token limit.
- Support message role formatting (`system`, `user`, `assistant`, `tool`).

### Tier 2: Episodic Memory with Multi-Factor Scoring
- Implement `EpisodicMemoryStore` with recency decay, importance ratings, and cosine similarity.
- Implement top-$k$ memory retrieval using weighted multi-factor scoring.

### Tier 3: Memory Reflection & Consolidation
- Implement `consolidate_memories()`: triggers when working memory fills up, extracting durable facts and flushing low-importance chatter.
