# Debug Lab 15 — Symptoms

> A caching and approximation layer: LRU eviction, a membership filter, a ring
buffer and an approximate distinct counter. These are the structures real
systems run on.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom — the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_cache_layer.py
echo "exit=$?"
```

There are **3** distinct defects.

---

## Symptom 1 — A cache hit does not protect an entry from eviction

```
[1] LRU cache
      capacity=2
          reported [1, 2, -1]
          expected [1, -1, 1]
      capacity=2
          reported [1, -1, 3]
          expected [1, 1, 3]
```

**Questions to answer:**

- Which entries in the reported lists differ from expected? Which key was evicted in each case?
- In the first case, key 1 is read just before key 3 is inserted. Under LRU, which key should be evicted at that point?
- Look at the `get` branch. It returns the value — does it do anything else?

## Symptom 2 — The membership filter says yes to almost everything

```
[2] Bloom filter membership
      inserted 800 items, queried the same 800
          false negatives: 0  (must be 0)
      queried 2000 never-inserted items
          reported present: 1194  (59.7%)
      a filter with 8192 bits and 800 items sets at most 2400 bits (29% of them)
```

**Questions to answer:**

- What percentage of the 2000 never-inserted items were reported present? Is that a useful filter?
- The last line says roughly what fraction of bits are set. If a query checks 3 positions, what is the chance that AT LEAST ONE of them is set by coincidence? What if it required ALL three?
- Compare the aggregation in the membership test with what is needed for the filter's guarantee. Should it be `any` or `all`?

## Symptom 3 — A full ring buffer overwrites the wrong slot

```
[3] Ring buffer with overwrite-oldest
      capacity=3 [('push', 1), ('push', 2), ('push', 3), ('push', 4), ('items', 0)]
          reported [[4, 2, 3]]
          expected [[2, 3, 4]]
      capacity=2 [('push', 1), ('push', 2), ('push', 3), ('pop', 0)]
          reported [3]
          expected [2]
      capacity=1 [('push', 1), ('push', 2), ('items', 0)]
          reported [[2]]
          expected [[2]]

====================================================================
Cache layer complete. Exit code 0.
====================================================================
```

**Questions to answer:**

- Which rows disagree? What state is the buffer in when it goes wrong?
- For capacity 3 pushed with 1,2,3,4, which value should have been discarded and what does the buffer actually hold?
- When the buffer is already full, a push overwrites the oldest entry. Two indices describe the buffer's contents — which of them must also move, and does it?

---

## How to verify a fix

Each defect breaks a property that a problem-bank test asserts:

| Symptom | Test that proves the fix |
| :--- | :--- |
| 1 | `test_p01_lru_cache` |
| 2 | `test_p02_bloom_filter` |
| 3 | `test_p04_ring_buffer` |

```bash
cd ../problems
python -m pytest tests -q
```

Fix the lab script in place. When its printed output matches what you reasoned
it should be, and you can name the property each defect violated, you are done.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
