# Debug Lab Solution & Forensic Post-Mortem

## Incident: Agentic RAG Answers Only the Last Sub-Question

---

### Forensic Root Cause Analysis
`gather_context()` keys the merged dictionary by each result's *rank
position within its own sub-question's result list*, not by the document's
identity:

```python
combined = {}
for sub_query in sub_queries:
    results = retrieve(sub_query)
    for rank, (doc_id, score) in enumerate(results):
        combined[rank] = (doc_id, score)
```

Every sub-question's retriever call returns a list starting at rank 0, so
`combined[0]` gets overwritten by each successive sub-question's top hit, and
`combined[1]` gets overwritten by each successive sub-question's second hit.
By the time the loop finishes, `combined` has exactly as many entries as the
*longest single sub-question's result list* (2, here), not the union of every
result across all sub-questions (6 retrievals, 4 distinct docs). Only the
last sub-question processed (`"How long does shipping take?"`) survives
completely -- everything from earlier sub-questions at the same rank
positions was silently clobbered.

---

### Production Corrective Action & Code Fix

```python
def gather_context(complex_query):
    sub_queries = decompose_query(complex_query)
    combined = {}
    for sub_query in sub_queries:
        results = retrieve(sub_query)
        for doc_id, score in results:
            # Key by the document's own identity, and keep the best score
            # seen for it across every sub-question that retrieved it.
            if doc_id not in combined or score > combined[doc_id][1]:
                combined[doc_id] = (doc_id, score)
    return combined
```

Keying by `doc_id` means every distinct document retrieved by any
sub-question survives into the merged context (with `doc_faq`, retrieved by
all three sub-questions, correctly keeping its best score), instead of being
silently clobbered by whichever sub-question happened to run last.

---

### Production Prevention Invariants
1. **Key Merges by Identity, Never by Position:** When combining results from
   multiple independent calls into one collection, the merge key must be the
   item's own identity (doc id, entity id, request id) -- a positional key
   like `rank` or loop index is only unique within a single call, not across
   calls.
2. **Union-Size Assertion:** After merging results from N independent
   retrievals, assert the merged set's size is bounded below by
   `len(set.union(*per_query_doc_ids))` minus expected true overlaps, not
   silently capped at the length of a single query's result list.
3. **Multi-Sub-Question Regression Test:** Agentic RAG pipelines need a test
   with sub-questions whose retrieved documents are known to be disjoint,
   asserting the final context contains evidence from every sub-question, not
   just the last one executed.
