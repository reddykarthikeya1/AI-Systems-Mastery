# Module 15 — Problem Bank

These are the structures you meet in real systems rather than in interviews,
and each one trades exactness for a resource.

* A **Bloom filter** trades correctness in one direction — it can say "maybe
  present" when the item is absent, but never "absent" when it is present. That
  asymmetry is the entire design, and problem 02's tests assert both halves.
* A **skip list** trades determinism for simplicity: expected `O(log n)` with
  no rotations, which is why Redis uses one for sorted sets.
* An **LRU cache** trades memory for O(1) eviction by pairing a hash map with a
  doubly linked list. Neither structure alone can do it.

**8 problems** · Easy 0 · Medium 1 · Hard 7

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
| 01 | [LRU Cache With O(1) Operations](p01_lru_cache.py) | Hash map + doubly linked list | Hard | `Time O(1) per operation, Space O(capacity)` |
| 02 | [Bloom Filter: No False Negatives](p02_bloom_filter.py) | Bloom filter | Hard | `Time O((n + q) * hashes), Space O(bits)` |
| 03 | [Skip List: Insert, Search, Delete](p03_skip_list.py) | Skip list | Hard | `Expected O(log n) per operation, Space O(n)` |
| 04 | [Fixed-Capacity Ring Buffer](p04_ring_buffer.py) | Circular buffer | Medium | `Time O(1) per operation, Space O(capacity)` |
| 05 | [LFU Cache](p05_lfu_cache.py) | Frequency buckets | Hard | `Time O(1) per operation, Space O(capacity)` |
| 06 | [Approximate Distinct Count](p06_hyperloglog.py) | Probabilistic cardinality estimation | Hard | `Time O(n), Space O(registers)` |
| 07 | [Count-Min Sketch: Frequency Estimation](p07_count_min_sketch.py) | Count-Min sketch | Hard | `Time O((n + q) * depth), Space O(width * depth)` |
| 08 | [Consistent Hashing Ring](p08_consistent_hash_ring.py) | Consistent hashing | Hard | `Time O((n*v) log(n*v) + k log(n*v)), Space O(n*v)` |

## Patterns covered

- Bloom filter
- Circular buffer
- Consistent hashing
- Count-Min sketch
- Frequency buckets
- Hash map + doubly linked list
- Probabilistic cardinality estimation
- Skip list

See [PATTERN_RECOGNITION_GUIDE.md](../../PATTERN_RECOGNITION_GUIDE.md) for how
to recognise each of these on a problem you have never seen.

---

## If you are stuck

Work the ladder in [Part 5 of the pattern guide](../../PATTERN_RECOGNITION_GUIDE.md).
The short version: re-read the constraints, do `n = 3` by hand, write the brute
force, then ask what the brute force repeats.

---

[Module README](../01_README.md) · [Pattern Guide](../../PATTERN_RECOGNITION_GUIDE.md)
