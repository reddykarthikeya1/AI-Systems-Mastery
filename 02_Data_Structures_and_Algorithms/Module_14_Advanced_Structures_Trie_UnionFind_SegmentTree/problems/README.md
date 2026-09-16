# Module 14 — Problem Bank

These three structures each answer a question the earlier ones cannot.

* A **hash map** cannot answer "which keys start with this prefix?" — a
  **trie** can, in `O(len(prefix))`.
* **DFS** can find connected components once; **union-find** answers "same
  group?" repeatedly *while* the graph is still changing.
* **Prefix sums** answer range queries in `O(1)` but cost `O(n)` per update; a
  **segment tree** makes both `O(log n)`.

Each is the right tool only when the workload matches. Union-find in particular
cannot *remove* an edge, which is worth knowing before you reach for it.

**8 problems** · Easy 0 · Medium 4 · Hard 4

---

## How to work these

```bash
cd problems
python -m pytest tests -q                 # all of this module's problems
python -m pytest tests -q -k p03          # just problem 3
```

Every problem must **fail** before you start — each stub raises
`NotImplementedError`. Fill in `pNN_<slug>.py`, not the solution file.

Each stub carries the statement, the constraints, a complexity target and a
**three-step hint ladder**. Read one hint, try again, and only then read the
next. Jumping to the reference solution costs you the exact skill the problem
exists to build.

When you are done, compare against `solutions/pNN_<slug>.py` — not to check the
answer, which the tests already did, but to compare *approach* and complexity.

---

## Problems

| # | Problem | Pattern | Difficulty | Target |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [Trie: Insert, Search, StartsWith](p01_trie_operations.py) | Trie | Medium | `Time O(len(word)) per operation, Space O(total characters)` |
| 02 | [Union-Find With Path Compression](p02_union_find.py) | Disjoint set union | Medium | `Time O(α(n)) amortised per op, Space O(n)` |
| 03 | [Segment Tree: Range Sum With Updates](p03_segment_tree.py) | Segment tree | Hard | `Time O(log n) per operation, Space O(n)` |
| 04 | [Find All Dictionary Words With A Prefix](p04_word_search_trie.py) | Trie traversal | Medium | `Time O(total chars + limit * len), Space O(total chars)` |
| 05 | [Accounts Merge](p05_accounts_merge.py) | Union-find over strings | Hard | `Time O(E log E) for the sort, Space O(E)` |
| 06 | [Sparse Table: Range Minimum, No Updates](p06_range_min_query.py) | Sparse table | Hard | `Time O(n log n) preprocessing, O(1) per query` |
| 07 | [Count Of Smaller Numbers After Self](p07_count_smaller_after.py) | Fenwick tree (BIT) | Hard | `Time O(n log n), Space O(n)` |
| 08 | [Prefix-Sum Map: Sum Of Keys With A Prefix](p08_implement_prefix_map.py) | Trie with aggregated values | Medium | `Time O(len(key)) per operation, Space O(total characters)` |

## Patterns covered

- Disjoint set union
- Fenwick tree (BIT)
- Segment tree
- Sparse table
- Trie
- Trie traversal
- Trie with aggregated values
- Union-find over strings

See [PATTERN_RECOGNITION_GUIDE.md](../../PATTERN_RECOGNITION_GUIDE.md) for how
to recognise each of these on a problem you have never seen.

---

## If you are stuck

Work the ladder in [Part 5 of the pattern guide](../../PATTERN_RECOGNITION_GUIDE.md).
The short version: re-read the constraints, do `n = 3` by hand, write the brute
force, then ask what the brute force repeats.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
