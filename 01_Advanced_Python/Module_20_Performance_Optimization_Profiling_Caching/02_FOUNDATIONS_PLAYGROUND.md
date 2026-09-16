# Interactive Foundations Playground: Performance Optimization, Profiling & Caching

> *"Premature optimization is the root of all evil; measure first, optimize where it counts."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to the **Module 20 Performance Optimization Profiling Caching** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

Optimization begins with measurement (profiling). The easiest 100x speedup in Python is **Caching** (memoization): storing expensive function results in RAM so you never compute the exact same input twice.

---

## 2. Micro-Code Example (3-5 Lines)

```python
import functools
import time

# Without caching, fib(35) takes seconds.
# With @lru_cache, it takes microseconds!
@functools.lru_cache(maxsize=128)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print("fib(35) =", fib(35))
```

### Line-by-Line Breakdown:
- `@functools.lru_cache(maxsize=128)`: Decorator that saves the return values of the last 128 unique function calls in a dictionary.
- `LRU`: Stands for Least Recently Used (discards the oldest items when cache is full).
- `cProfile`: Built-in Python profiler that reveals which functions consume the most time.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
Can you cache a function that takes a mutable list as an argument?

<details><summary><b>Show Answer</b></summary>

**No!** Cache keys must be hashable. Lists are mutable and cannot be hashed; use tuples instead.
</details>

---

### Drill 2: Quick Check
What does LRU stand for?

<details><summary><b>Show Answer</b></summary>

Least Recently Used.
</details>

---
