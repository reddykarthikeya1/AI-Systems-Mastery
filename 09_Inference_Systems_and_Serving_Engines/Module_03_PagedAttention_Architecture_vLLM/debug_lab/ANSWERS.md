# Debug Lab Solution & Forensic Post-Mortem

## Incident: Beam Search Forks Bleed Tokens Into Each Other

---

### Forensic Root Cause Analysis
`fork()` correctly shares the physical blocks and bumps `refcount`:

```python
def fork(self, new_name):
    child = PagedSequence(new_name, self.block_pool)
    child.block_table = list(self.block_table)
    for block in child.block_table:
        block.refcount += 1
    return child
```

But `append_token()` never checks that refcount before writing:

```python
def append_token(self, token):
    ...
    last_block = self.block_table[-1]
    last_block.tokens.append(token)
```

After the fork, block 0 has `refcount == 2` and is referenced from *both*
`parent.block_table[-1]` and `child.block_table[-1]` -- it is the literal same
Python object in memory, not a copy. When `parent.append_token("France")`
runs, it mutates that shared object's `.tokens` list in place, so `child`
(which points at the same object) immediately sees `"France"` too. Then
`child.append_token("Germany")` appends onto the now-shared, already-mutated
list, landing both tokens on the object the child holds while the parent's own
view of the same object only reflects the last write. This is exactly the bug
copy-on-write exists to prevent: a block with `refcount > 1` must never be
mutated in place.

---

### Production Corrective Action & Code Fix

```python
def append_token(self, token):
    if not self.block_table or len(self.block_table[-1].tokens) == BLOCK_SIZE:
        new_block = PhysicalBlock(len(self.block_pool))
        self.block_pool.append(new_block)
        self.block_table.append(new_block)
    last_block = self.block_table[-1]
    if last_block.refcount > 1:
        # Copy-on-write: this block is shared, so split off a private copy
        # before mutating it, and drop this sequence's reference to the
        # shared original.
        private_block = PhysicalBlock(len(self.block_pool))
        private_block.tokens = list(last_block.tokens)
        self.block_pool.append(private_block)
        last_block.refcount -= 1
        self.block_table[-1] = private_block
        last_block = private_block
    last_block.tokens.append(token)
```

With the fix, the moment `parent` or `child` writes into a shared block, that
sequence gets its own private copy first, so `parent` ends with
`['The', 'capital', 'of', 'France']` and `child` ends with
`['The', 'capital', 'of', 'Germany']`, independently.

---

### Production Prevention Invariants
1. **Refcount Gates Mutation:** Any block with `refcount > 1` is read-only by
   definition; every write path must check refcount and copy-on-write before
   touching `.tokens`, not just the allocator.
2. **Identity vs. Value Sharing Tests:** Regression tests for fork/branch
   operations should assert object identity diverges after a write, not just
   that the values look right immediately after the fork.
3. **Beam Search Isolation Test:** Any parallel-sampling or beam-search path
   should have a test that forks a sequence, diverges both branches by one
   token each, and asserts neither branch's tail leaks into the other.
