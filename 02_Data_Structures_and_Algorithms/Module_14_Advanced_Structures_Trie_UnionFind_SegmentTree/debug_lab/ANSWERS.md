# Debug Lab 14 — Answers

> Read this only after you have written a diagnosis for each symptom.

3 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — Searching for a prefix reports it as a stored word

**Location:** `simulate_trie`, the `search` branch

**The bug:**

```python
elif name == "search":
    out.append(walk(arg) is not None)       # identical to starts_with
```

**The fix:**

```python
elif name == "search":
    node = walk(arg)
    # The end-of-word flag is what separates a stored word from a mere prefix.
    out.append(bool(node is not None and node["is_word"]))
```

**Why it matters.** `is_word` is set on insert and then never read, so `search` and `starts_with` are
literally the same operation. Every prefix of every stored word is reported as a
stored word.

Both answers are booleans and both are right whenever the query happens to be a
complete word, so a test set built from inserted words passes completely. It only
fails on a proper prefix — which is the one case that distinguishes the two
operations.

If two branches of a dispatch have identical bodies, either one is wrong or the
distinction is meaningless. Here the flag that encodes the distinction was
maintained and ignored.

**Proved by:** `test_p01_trie_operations`

## Defect 2 — Union-find degrades to a linked list

**Location:** `simulate_union_find`, the `find` helper and the `union` merge

**The bug:**

```python
def find(x):
    while parent[x] != x:
        x = parent[x]       # no path compression
    return x
...
parent[rb] = ra             # no union by size: the tree grows ever deeper
```

**The fix:**

```python
def find(x):
    root = x
    while parent[root] != root:
        root = parent[root]
    # Path compression: point everything on the path straight at the root.
    while parent[x] != root:
        parent[x], x = root, parent[x]
    return root

# Union by size keeps the trees shallow.
if size[ra] < size[rb]:
    ra, rb = rb, ra
parent[rb] = ra
size[ra] += size[rb]
```

**Why it matters.** Without path compression or union by size, merging a chain in order builds a
degenerate tree one node deep per union. `find` then walks the whole chain, and
the structure whose entire selling point is near-constant-time operations becomes
linear.

Every answer stays correct, so no correctness test will ever notice. What changes
is the complexity class: at 10⁵ elements the difference is roughly 10⁵ operations
versus 10¹⁰.

The two optimisations are not micro-tuning. They are what make the data structure
the data structure, and omitting them leaves you with an array of pointers that
happens to give right answers slowly.

**Proved by:** `test_p02_union_find`

## Defect 3 — Range sums go stale after an update

**Location:** `simulate_segment_tree`, the `update` branch

**The bug:**

```python
if name == "update":
    i = a + n
    tree[i] = b         # the leaf is written; its ancestors are never recomputed
```

**The fix:**

```python
if name == "update":
    i = a + n
    tree[i] = b
    # Walk up recomputing every ancestor from its two children.
    i //= 2
    while i >= 1:
        tree[i] = tree[2 * i] + tree[2 * i + 1]
        i //= 2
```

**Why it matters.** The whole point of a segment tree is that internal nodes cache the sums of their
subtrees. Writing a leaf without repairing that cache leaves every ancestor
holding a sum computed from the old value.

Queries answered entirely from leaves stay correct, and so do queries that
predate the update — which is why the first query in each case looks fine. Only
queries spanning a range wide enough to be answered from an internal node return
the stale figure, so the errors appear to come and go with the query shape.

Any structure that caches derived values owes an invalidation path. Writing the
source without repairing the cache is a wrong answer waiting for the right
query.

**Proved by:** `test_p03_segment_tree`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | Searching for a prefix reports it as a stored word | No |
| 2 | Union-find degrades to a linked list | No |
| 3 | Range sums go stale after an update | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
