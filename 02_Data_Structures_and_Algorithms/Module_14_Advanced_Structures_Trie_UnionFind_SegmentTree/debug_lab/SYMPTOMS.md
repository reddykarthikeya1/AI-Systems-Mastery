# Debug Lab 14 — Symptoms

> An indexing service: prefix search, group membership, range sums and rank
counting. Each structure is almost right.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_index_structures.py
echo "exit=$?"
```

There are **3** distinct defects.

---

## Symptom 1 — Searching for a prefix reports it as a stored word

```
[1] Trie: search vs starts_with
      ops = [('insert', 'apple'), ('search', 'apple'), ('search', 'app'), ('starts_with', 'app'), ('insert', 'app'), ('search', 'app')]
          reported [True, True, True, True]
          expected [True, False, True, True]
      ops = [('insert', 'hello'), ('search', 'hell'), ('search', 'he'), ('starts_with', 'hell')]
          reported [True, True, True]
          expected [False, False, True]
```

**Questions to answer:**

- Which entries disagree with the expected list? Are the `search` results or the `starts_with` results wrong?
- After inserting only `"apple"`, is `"app"` a word that was stored? What did `search` say?
- Compare the `search` branch with the `starts_with` branch. What is different between them, and what *should* be different?

## Symptom 2 — Union-find degrades to a linked list

```
[2] Union-find: connectivity (with timing)
      chain of 4000   + 400   lookups -> connected=True took     34.56 ms
      chain of 16000  + 1600  lookups -> connected=True took    554.45 ms
      (both the chain AND the lookup count quadrupled - what did the time do?)
```

**Questions to answer:**

- The answers are correct. Read the elapsed-time column: the chain grew by 4x. By what factor did the time grow?
- After `union(0,1)`, `union(1,2)`, `union(2,3)`, …, draw the parent pointers. What shape is the tree?
- How many pointer hops does `find(n-1)` take on that shape? What is the operation supposed to cost?

## Symptom 3 — Range sums go stale after an update

```
[3] Segment tree: range sums with updates
      [1, 3, 5] [('query', 0, 2), ('update', 1, 2), ('query', 0, 2)]
          reported [9, 9]
          expected [9, 8]
      [1, 2, 3, 4] [('query', 0, 3), ('update', 0, 10), ('query', 0, 3)]
          reported [10, 10]
          expected [10, 19]
```

**Questions to answer:**

- Which queries disagree? Are the ones BEFORE the update correct?
- A segment tree stores internal nodes holding the sums of their children. When a leaf changes, which other nodes' values become wrong?
- Find the code that writes the new leaf value. What happens after that write?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p01_trie_operations` |
| 2 | `test_p02_union_find` |
| 3 | `test_p03_segment_tree` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
