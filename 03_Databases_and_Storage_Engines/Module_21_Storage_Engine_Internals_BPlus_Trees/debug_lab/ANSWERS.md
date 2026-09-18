# Debug Lab Solution & Forensic Post-Mortem

## Incident: Deadlock in Concurrent B+ Tree Node Split

---

### 🔍 Forensic Root Cause Analysis
`search_buggy()` releases the parent latch and captures a plain object
reference to the child node (`target_node = self.child`) *before* accounting
for a concurrent structural change. A split happening in that window moves
half of the child's keys into a new sibling node. Because proper lock
coupling ("crabbing") was violated -- the parent latch was given up without
first validating the child against a concurrent split -- the traversal ends
up searching a node that no longer contains the full set of keys it is
responsible for, silently reporting a key as missing when it has simply moved
to the new sibling.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def search_correct(self, key):
    """Lock coupling ("crabbing"): hold the parent latch until the child
    latch is acquired, and re-check for a split before releasing either."""
    # acquire child latch WHILE still holding the parent latch
    node = self.child
    # only now, with the child latch held, is it safe to release the parent
    if self.sibling is not None and key in self.sibling.keys:
        return key in self.sibling.keys
    return key in node.keys
```

The durable fix is structural: never release a parent (or any ancestor)
latch until the next latch down the path has been acquired, so no concurrent
split can invalidate a pointer the traversal is about to follow.

---

### 🛡️ Production Prevention Invariants
1. **Strict lock coupling / crabbing** on every downward traversal: acquire
   child before releasing parent, always.
2. **Structural-change counters (SMOs)** that force a traversal to retry if a
   split/merge happened during descent.
3. **Concurrency stress tests** that interleave reads with concurrent splits
   and assert no key is ever silently lost.
