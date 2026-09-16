# Debug Lab 15 — Answers

> Read this only after you have written a diagnosis for each symptom.

3 defects. Every one produces a plausible wrong answer rather
than a crash, which is why the exit code is 0.

---

## Defect 1 — A cache hit does not protect an entry from eviction

**Location:** `simulate_lru`, the `get` branch

**The bug:**

```python
if name == "get":
    if key in cache:
        out.append(cache[key])      # returns the value but does not mark it used
```

**The fix:**

```python
if name == "get":
    if key in cache:
        cache.move_to_end(key)      # a hit IS a use, and refreshes recency
        out.append(cache[key])
```

**Why it matters.** In an LRU cache, reading an entry is a use — that is what the "recently used"
in the name refers to. Without refreshing recency on a hit, the ordering reflects
insertion time only, and the policy silently degrades to FIFO.

The cache still returns correct values for everything it holds, and still evicts
when full, so it behaves like a working cache. What changes is *which* entries
survive: the hottest key in the workload is evicted on schedule alongside keys
nobody has touched, and the hit rate quietly collapses under load.

A performance-shaped bug with no functional symptom is the hardest kind to find
from the outside. The only reliable detection is an eviction-order assertion.

**Proved by:** `test_p01_lru_cache`

## Defect 2 — The membership filter says yes to almost everything

**Location:** `bloom_check`, the membership test

**The bug:**

```python
return [any(bitset[p] for p in positions(q)) for q in queries]      # any
```

**The fix:**

```python
# ALL bits must be set. `any` produces both false positives AND false
# negatives; `all` is what makes false negatives impossible.
return [all(bitset[p] for p in positions(q)) for q in queries]
```

**Why it matters.** A Bloom filter's contract is one-sided: it may say "maybe present" for an item
that is absent, but never "absent" for one that was inserted. `any` does not
break that guarantee — an inserted item still has all its bits set, so at least
one of them is certainly set. The false-negative count stays 0.

What `any` destroys is the filter's *usefulness*. It reports present whenever a
single one of the query's bits collides with any bit set by any item, so the
false-positive rate rises from a fraction of a percent to a large share of all
queries. A filter that says yes to most of what you ask it saves no work at all
— which is the only reason to have one.

This is worth dwelling on because the failure is entirely quantitative. Nothing
raises, the stated guarantee still holds, and every individual answer is
*permitted* by the contract. Only the rate reveals it, and only if you measure.

**Proved by:** `test_p02_bloom_filter`

## Defect 3 — A full ring buffer overwrites the wrong slot

**Location:** `simulate_ring_buffer`, the `push` branch when full

**The bug:**

```python
buf[(head + count) % capacity] = value
if count < capacity:
    count += 1
# when full, the write lands on the oldest slot but `head` never advances
```

**The fix:**

```python
buf[(head + count) % capacity] = value
if count < capacity:
    count += 1
else:
    # Full: the write consumed the oldest slot, so the head moves with it.
    head = (head + 1) % capacity
```

**Why it matters.** When the buffer is full, `(head + count) % capacity` is exactly `head` — the
oldest slot. The new value lands there correctly, but `head` still points at it,
so the buffer now believes the newest entry is the oldest.

The contents and the count stay plausible; only the ordering is wrong, and it
only goes wrong once the buffer has filled. A test that never reaches capacity
passes completely.

Two indices define a ring buffer's state and both move on an overwrite. Whenever
a data structure keeps redundant state, enumerate every field a mutation touches
— the compiler will not.

**Proved by:** `test_p04_ring_buffer`

---

## Scoreboard

| # | Defect | Would a crash-based test have caught it? |
| :-- | :--- | :--- |
| 1 | A cache hit does not protect an entry from eviction | No |
| 2 | The membership filter says yes to almost everything | No |
| 3 | A full ring buffer overwrites the wrong slot | No |

Not one of these raises. That is the whole point of the exercise: in
algorithms, **a green run is not evidence of a correct answer.** The only
reliable evidence is a property asserted against an independent computation —
which is why every problem in this course's bank is cross-checked against a
brute force, a library function, or a second implementation.

---

[Module README](../01_README.md) · [Symptoms](SYMPTOMS.md)
