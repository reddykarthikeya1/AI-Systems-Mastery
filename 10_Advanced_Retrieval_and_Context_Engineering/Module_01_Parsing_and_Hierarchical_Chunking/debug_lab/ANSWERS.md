# Debug Lab Solution & Forensic Post-Mortem

## Incident: Facts Straddling a Chunk Boundary Vanish From Retrieval

---

### Forensic Root Cause Analysis
`chunk_document()` accepts an `overlap` parameter but never uses it when
advancing the window:

```python
while start < len(text):
    end = start + chunk_size
    chunks.append(text[start:end])
    start = end  # advance to the next non-overlapping window
```

`start = end` moves the window forward by exactly `chunk_size` every
iteration, so each new chunk begins precisely where the previous one ended --
zero characters are shared between consecutive chunks. The `overlap`
parameter is dead code: it's threaded through the function signature and the
module-level constant is defined, but nothing in the loop body subtracts it
from the advance. Any sentence or fact whose character span crosses a
`chunk_size`-aligned cut point -- like `"received. Section 2"` crossing the
boundary at character 80 -- gets split so that neither resulting chunk
contains the full phrase, and a similarity search for that phrase can only
ever partially match one side of it.

---

### Production Corrective Action & Code Fix

```python
def chunk_document(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # step back by `overlap` so the tail of this
                                # chunk reappears at the head of the next one
    return chunks
```

With the fix, each new chunk starts `overlap` characters before the previous
chunk ended, so `"received. Section 2"` appears whole inside the chunk that
begins at the overlapped start position, and boundary-straddling facts are
retrievable from at least one chunk.

---

### Production Prevention Invariants
1. **Wire Every Configured Parameter Into Behavior:** An `overlap` (or any
   tunable) that's accepted as a parameter but never referenced in the logic
   is a defect waiting to be found -- treat unused parameters as a code smell,
   not a stylistic nit.
2. **Boundary-Straddling Fixture Test:** Chunkers should be tested with a
   document constructed so a known phrase deliberately straddles a
   `chunk_size`-aligned cut, and assert that phrase survives intact in at
   least one chunk.
3. **Advance-Step Invariant:** Assert `next_start < previous_end` whenever
   `overlap > 0` is configured -- if the window's start never lands before
   the previous window's end, overlap isn't actually happening regardless of
   what the config says.
