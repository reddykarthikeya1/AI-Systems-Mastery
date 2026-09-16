# Module 20: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Performance Optimization, Profiling, and Caching before moving to **Module 19**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **cProfile Metrics:** In `cProfile` statistics, what is the difference between `tottime` (total time) and `cumtime` (cumulative time)?
2. **Fast Serialization:** Why is Rust-backed `orjson` significantly faster at serializing JSON than standard library `json`?
3. **Cache-Aside Pattern:** Explain the sequential read steps when an application implements the Cache-Aside pattern.
4. **Cache Stampede:** What is a Cache Stampede (Thundering Herd), and why can it take down production databases on hot key expiry?
5. **Cache Avalanche:** What is a Cache Avalanche, and how does adding random TTL jitter prevent it?
6. **Cache Penetration:** What is Cache Penetration, and how does caching null values or using a Bloom Filter solve it?
7. **Local vs Distributed Cache:** When should you use `functools.lru_cache` (local process) vs Redis (distributed cluster)?
8. **RAM Profiling:** What Python module is built into standard library to track memory allocations and detect RAM leaks?
9. **`__slots__` Efficiency:** How does `__slots__` reduce memory footprint when storing 1,000,000 dataclass instances?
10. **Database Indexing:** Why does an SQL B-Tree index turn an $O(N)$ full table scan into an $O(\log N)$ index seek?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
- `tottime`: Total time spent directly inside that specific function, *excluding* calls to sub-functions.
- `cumtime`: Cumulative time spent inside that function *plus* all sub-functions called by it.

#### Answer 2:
`orjson` is written in Rust, leverages SIMD CPU instructions for direct memory copies, and bypasses Python object creation bottlenecks during string encoding.

#### Answer 3:
1. Application queries Cache with key.
2. If **Hit**: Return cached data immediately.
3. If **Miss**: Query database, store result in cache with TTL, and return result.

#### Answer 4:
When a highly-requested cache key expires, thousands of concurrent requests miss the cache simultaneously and storm the database with identical heavy queries.

#### Answer 5:
A massive batch of keys expiring at the exact same second. Adding random jitter (e.g. $\pm 10\%$) distributes expirations smoothly over time.

#### Answer 6:
Attackers querying non-existent keys repeatedly to bypass the cache and hit the database. Caching a short-lived `None` or checking a **Bloom Filter** rejects non-existent keys before touching the DB.

#### Answer 7:
- `lru_cache`: In-memory in the single Python process (fastest, but memory is duplicated across multi-worker processes).
- `Redis`: Centralized network cache shared across all web workers and containers.

#### Answer 8:
**`tracemalloc`**.

#### Answer 9:
By suppressing the dynamic `__dict__` hash table allocation on each instance, storing attributes in fixed-size C structs (saving up to $60\%$ RAM).

#### Answer 10:
B-Tree indexes maintain sorted balanced tree structures allowing binary search lookups in logarithmic time ($O(\log N)$) instead of scanning every raw row on disk.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: TTL-Aware In-Memory Cache Decorator

**Goal:** Create a decorator `@cached_with_ttl(seconds=5)` that caches function results in a dict with an expiration timestamp.

<details>
<summary><b>Solution Code</b></summary>

```python
import functools
import time

def cached_with_ttl(seconds: float = 5.0):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache:
                val, exp = cache[args]
                if now < exp:
                    return val
            res = func(*args)
            cache[args] = (res, now + seconds)
            return res
        return wrapper
    return decorator

# Verification:
@cached_with_ttl(seconds=2.0)
def compute(x): return x * 2

print("First call (computed):", compute(10))
print("Second call (cached) :", compute(10))
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Wall-clock TTL

```python
import time

def set_with_ttl(store: dict, key: str, value: object, ttl: float) -> None:
    store[key] = (value, time.time() + ttl)
```

**Observed symptom:** After the server's clock is corrected backwards by NTP, cached entries live for hours. After a forward correction, the entire cache expires at once and the database is overwhelmed.

**(a)** Why is `time.time()` wrong for a deadline?

**(b)** What is the one-word fix?

**(c)** Which test in this course would have caught it?

<details>
<summary><b>Show the diagnosis</b></summary>

`time.time()` is the **wall clock**. It is not monotonic: NTP corrections, DST changes and manual adjustments move it in either direction. A deadline computed from it is meaningless after any such jump.

**Fix:** `time.monotonic()`, which only ever increases and is unaffected by clock changes. Use it for every interval, timeout, and deadline. Reserve `time.time()` for timestamps you intend to *display* or store.

**The test:** `Module_20/project_solution/test_cache_engine.py::test_ttl_uses_monotonic_clock_not_wall_clock` — it monkeypatches `time.time` to 0 and to 9999999999 and asserts a live entry survives both. That is how you pin a property that is otherwise invisible in normal operation.

</details>

---

### D2. Cached None treated as a miss

```python
def get_or_load(cache: dict, key: str, loader) -> object:
    value = cache.get(key)
    if value is None:
        value = loader()
        cache[key] = value
    return value
```

**Observed symptom:** A lookup that legitimately returns `None` re-hits the database on every single request. The cache hit ratio for that key is 0%.

**(a)** Why can this cache never store a null result?

**(b)** What is the standard fix?

**(c)** Why is this bug so easy to miss in testing?

<details>
<summary><b>Show the diagnosis</b></summary>

`None` is overloaded to mean both 'absent from cache' and 'the cached value is null'. A stored `None` is indistinguishable from a miss, so the loader runs forever.

**Fix:** a unique **sentinel** object.

```python
MISSING = object()
value = cache.get(key, MISSING)
if value is MISSING:
    ...
```

Module 20's `cache_engine.py` uses exactly this, and returns `MISSING` rather than `None` from `get`.

**Easy to miss** because the code is *functionally correct* — every response is right, nothing errors, no test fails. It is purely a performance defect, and only visible if you assert on hit/miss *counters* rather than on return values. See `test_cached_none_is_a_hit_not_a_miss`, which asserts `stats.misses == 0`.

</details>

---

### D3. Cache stampede

```python
async def get_popular(key: str) -> dict:
    cached = await cache.get(key)
    if cached is not None:
        return cached
    result = await expensive_db_query(key)     # 300 ms
    await cache.set(key, result, ttl=60)
    return result
```

**Observed symptom:** Every 60 seconds the database CPU spikes to 100% and latency jumps to 4 s. Between spikes everything is fine.

**(a)** What happens at the instant the key expires?

**(b)** What is the fix called, and how does it work?

**(c)** Name one alternative mitigation.

<details>
<summary><b>Show the diagnosis</b></summary>

At expiry, every concurrent request misses simultaneously. With 500 requests in flight, all 500 call `expensive_db_query` at once — a **cache stampede** (or dogpile). The database sees a 500× spike for the duration of one query.

**Fix: single-flight.** The first caller acquires a per-key lock and performs the load; every other caller waits on an `Event` and receives the same result. One query instead of 500. Module 20's `TwoTierCache.get_or_load` implements this, and `test_single_flight_prevents_stampede` asserts the loader ran exactly once.

**Alternative:** **probabilistic early expiration** (XFetch) — each reader refreshes slightly early with a probability that rises as expiry approaches, so refreshes are spread out and no synchronised cliff exists. Staggered TTLs with jitter achieve a weaker version of the same thing.

</details>

---

### D4. Benchmark measuring the wrong thing

```python
import time

start = time.time()
result = compute()
print(f"took {time.time() - start}s")
```

**Observed symptom:** The same code reports 0.0 s sometimes and 0.03 s other times, and results differ wildly between runs.

**(a)** Name two separate defects in this measurement.

**(b)** What is the correct approach?

**(c)** Why take the minimum of N runs rather than the mean?

<details>
<summary><b>Show the diagnosis</b></summary>

**Two defects.** (1) `time.time()` has coarse resolution on some platforms (~16 ms on Windows historically) and is subject to clock adjustment — use `time.perf_counter()`. (2) A single measurement is dominated by noise: OS scheduling, CPU frequency scaling, cache state, and any concurrent process.

**Correct:** `timeit` or an explicit loop of N runs with `perf_counter`, after a warm-up iteration to populate caches and trigger any lazy imports.

**Minimum, not mean:** noise is strictly *additive* — an interrupt can only make a run slower, never faster. The minimum is therefore the closest estimate of the code's intrinsic cost, while the mean measures your machine's background load. Report the mean only when you care about the distribution (tail latency), and then report percentiles rather than an average.

</details>

---

### D5. Optimising without profiling

```python
# "Optimised" list building
result = []
for i in range(1000):
    result.append(transform(i))

# rewritten as:
result = [transform(i) for i in range(1000)]
```

**Observed symptom:** The comprehension is measurably faster in isolation, but the endpoint's p99 latency does not change at all.

**(a)** Why did a genuine micro-optimisation have no effect?

**(b)** What should have been done first?

**(c)** What is the rule of thumb for where to look?

<details>
<summary><b>Show the diagnosis</b></summary>

The loop was never the bottleneck. A comprehension saves perhaps 30 µs here; if `transform` makes a database call taking 20 ms, the loop is 0.15% of the time.

**Do first:** profile. `cProfile` with `SnakeViz` for a call-graph view, or `py-spy` to sample a running production process without restarting it. Find the function with the largest **cumulative** time, not the largest self time — that is where the wall clock actually goes.

**Rule of thumb:** in a typical web service the order of suspicion is I/O (database, network, disk) → serialisation → algorithmic complexity → interpreter overhead. Interpreter overhead is *last*, which is why Module 22 insists you measure, vectorise and cache before reaching for Rust. Optimising an unprofiled guess is how people spend a week for a 0.15% gain.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites a real file or test in this course. Open them —
the fix is not hypothetical, it is in the code you already have.
