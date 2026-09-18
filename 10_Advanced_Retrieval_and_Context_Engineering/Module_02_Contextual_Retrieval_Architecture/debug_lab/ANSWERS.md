# Debug Lab Solution & Forensic Post-Mortem

## Incident: Contextual Retrieval Returns the Wrong Policy Chunk, and One Topic Is Unsearchable

---

### Forensic Root Cause Analysis
`contextualize_chunks()` generates one context sentence per chunk (correctly
index-aligned: `contexts[i]` describes `chunks[i]`), but then pairs them up
with an off-by-one slice:

```python
contexts = [generate_context(i) for i in range(len(chunks))]
paired = list(zip(contexts[1:], chunks))
```

`contexts[1:]` drops `contexts[0]` (the refund chunk's own context) and
shifts every remaining context one position earlier relative to `chunks`, so
`contexts[1]` (exchange's context) gets paired with `chunks[0]` (refund's raw
text), and `contexts[2]` (shipping's context) gets paired with `chunks[1]`
(exchange's raw text). Because `zip()` silently truncates to the shorter of
its two inputs -- `len(contexts[1:]) == 2` while `len(chunks) == 3` --
`chunks[2]` (the shipping chunk) never appears in `paired` at all and is
dropped from the embedded index entirely, not just mislabeled. The query
"How long does international shipping take?" can now only match on the stray
word "shipping" inside the misapplied context sentence prepended to the
exchange chunk, retrieving policy text about exchanges instead of shipping,
while the real shipping content is permanently unreachable.

---

### Production Corrective Action & Code Fix

```python
def contextualize_chunks(chunks):
    contexts = [generate_context(i) for i in range(len(chunks))]
    paired = list(zip(contexts, chunks))  # each chunk keeps its OWN context
    return [f"{ctx} {chunk}" for ctx, chunk in paired]
```

Removing the `[1:]` slice restores the index alignment `contexts[i]` <->
`chunks[i]` for every chunk, so all 3 source chunks are embedded, each with
its own correct topic sentence, and the shipping query now matches the
shipping chunk.

---

### Production Prevention Invariants
1. **Assert Corpus Size Is Preserved:** Any indexing pipeline stage should
   assert `len(output) == len(input)` (or explicitly justify a difference);
   `zip()` silently truncating unequal-length iterables is a common source of
   quietly dropped records.
2. **Index-Alignment Test:** When pairing two parallel lists produced from
   the same source (contexts and chunks, here), test that
   `paired[i]` corresponds to `chunks[i]` by construction, not by an
   assumption about slicing.
3. **Per-Chunk Retrievability Audit:** Periodically verify every chunk in the
   source corpus is retrievable by at least one representative query;
   "vanished from the index" bugs like this one don't raise errors and are
   invisible without an explicit coverage check.
