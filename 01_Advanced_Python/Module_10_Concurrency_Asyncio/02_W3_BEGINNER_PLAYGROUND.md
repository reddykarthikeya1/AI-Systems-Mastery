# W3Schools-Style Playground: AsyncIO & Coroutines

> *"Async is not multiple people; it is one organized person juggling multiple tasks."*

Welcome to the **Module 10 Concurrency Asyncio** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

AsyncIO lets a single Python process handle thousands of waiting operations (like web requests) without spawning thousands of threads. You mark functions with `async def` and use `await` to yield control while waiting.

---

## 2. Micro-Code Example (3-5 Lines)

```python
import asyncio

async def fetch_item(id_num):
    print(f"[*] Fetching item #{id_num}...")
    await asyncio.sleep(0.5)  # Yield CPU while waiting!
    print(f"[OK] Got item #{id_num}")
    return f"Item-{id_num}"

async def main():
    # Run both fetches concurrently on 1 single thread:
    items = await asyncio.gather(fetch_item(1), fetch_item(2))
    print("Results:", items)

asyncio.run(main())
```

### Line-by-Line Breakdown:
- `async def`: Defines a **coroutine function** instead of a regular synchronous function.
- `await`: Pauses this specific coroutine and gives CPU time back to the event loop so other coroutines can run.
- `asyncio.gather()`: Bundles multiple coroutines to run concurrently.
- `asyncio.run()`: Boots the event loop and executes the main coroutine to completion.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
Can you use `time.sleep()` inside an `async def` function?

<details><summary><b>Show Answer</b></summary>

**No!** `time.sleep()` freezes the entire thread and blocks the event loop. Always use `await asyncio.sleep()` in async code.
</details>

---

### Drill 2: Quick Check
What does an `async def` function return if called without `await`?

<details><summary><b>Show Answer</b></summary>

It returns an unexecuted coroutine object and issues a `RuntimeWarning`.
</details>

---
