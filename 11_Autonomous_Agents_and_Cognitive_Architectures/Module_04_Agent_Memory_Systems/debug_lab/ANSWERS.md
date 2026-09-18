# Debug Lab Solution & Forensic Post-Mortem

## Incident: Agent Memory Store Grows Without Bound and Buries the One Relevant Fact at the End of the List

---

### 🔍 Forensic Root Cause Analysis
`add_memory()` unconditionally appends to `self.memories` with no cap, eviction policy, or summarization step, so the list grows by exactly one entry per turn for the entire lifetime of the session -- 500 turns means 500 entries held in memory and replayed into every future prompt. `retrieve()` compounds this by ignoring its own `query` argument entirely:

```python
def retrieve(self, query):
    return self.memories
```

Every call returns the complete, unranked memory list regardless of what was asked, so callers receive the entire ever-growing history rather than the handful of memories actually relevant to the current query. The one memory that answers the query isn't surfaced or prioritized in any way -- it simply sits wherever insertion order happened to put it, which in this run means dead last, after 500 irrelevant entries.

---

### 🛠️ Production Corrective Action & Code Fix

```python
class FixedMemoryStore:
    def __init__(self, max_memories=200):
        self.memories = []
        self.max_memories = max_memories

    def add_memory(self, content):
        self.memories.append(content)
        if len(self.memories) > self.max_memories:
            self.memories.pop(0)  # evict oldest; production systems would summarize/archive instead

    def retrieve(self, query, top_k=5):
        scored = sorted(self.memories, key=lambda m: _relevance(query, m), reverse=True)
        return scored[:top_k]
```

Capping `self.memories` bounds worst-case growth by design instead of letting it scale with conversation length indefinitely. Scoring candidates against `query` and returning only the top-`k` means retrieval calls actually filter for relevance instead of echoing the entire store back on every request.

---

### 🛡️ Production Prevention Invariants
1. **Bound Memory Store Size Explicitly:** Growth must be capped by an eviction or summarization strategy defined up front, not discovered as an incident when the context window overflows.
2. **`retrieve()` Must Score and Truncate:** Any memory-retrieval call must rank candidates against the query and return only the top-k most relevant results, never the entire store.
3. **Track Prompt Token Counts From Retrieved Memories:** Monitor the size of what retrieval hands back over time so unbounded growth or ranking regressions are caught before they exhaust the context window in production.
