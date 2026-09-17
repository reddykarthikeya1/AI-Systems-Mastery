# 🐣 Interactive Foundations Playground: Performance Optimization: Profiling & Caching

> *"Measure before optimizing; cache aggressively to turn compute into memory lookup."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import functools
import time
```

---

## 1. LRU Caching with functools.lru_cache

`lru_cache` memoizes function returns to eliminate redundant expensive computations.

```python
call_count = 0
@functools.lru_cache(maxsize=128)
def expensive_calculation(n):
    global call_count
    call_count += 1
    return n * n

res1 = expensive_calculation(10)
res2 = expensive_calculation(10)
assert res1 == 100
assert res2 == 100
assert call_count == 1
assert expensive_calculation.cache_info().hits == 1
print(f"LRU cache hit: computation executed {call_count} time(s).")
```

---

## 2. Microbenchmarking Code Sections

`time.perf_counter` measures execution duration with high monotonic resolution.

```python
t0 = time.perf_counter()
total = sum(i for i in range(10_000))
elapsed = time.perf_counter() - t0
assert total == 49995000
assert elapsed >= 0
print(f"Summed 10,000 numbers in {elapsed*1000:.4f} ms.")
```

---

## 3. String Concatenation Optimization

Joining a list of strings is $O(N)$, whereas repeated `+=` string concatenation is $O(N^2)$.

```python
parts = [f"item_{i}" for i in range(100)]
joined = ",".join(parts)
assert len(joined.split(",")) == 100
assert joined.startswith("item_0")
assert joined.endswith("item_99")
print(f"Joined {len(parts)} tokens cleanly with O(N) memory allocation.")
```

---
