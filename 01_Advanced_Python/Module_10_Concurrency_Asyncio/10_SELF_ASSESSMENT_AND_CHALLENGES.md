# Module 10: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Asyncio, the Event Loop, Coroutines, and TaskGroups before moving to **Module 11**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Multitasking Models:** What is the technical difference between Cooperative Multitasking (used by Asyncio) and Preemptive Multitasking (used by OS Threads)?
2. **The `await` Keyword:** When Python encounters an `await` expression, what exactly happens to the current coroutine and the Event Loop?
3. **Loop Freezes:** Why is executing `time.sleep(5)` inside an async coroutine considered a critical bug, and what should you write instead?
4. **Structured Concurrency:** What advantage does `asyncio.TaskGroup` (Python 3.11+) provide over legacy `asyncio.gather()` when one of several concurrent tasks crashes?
5. **Rate Limiting:** How does `asyncio.Semaphore(10)` protect backend APIs and database connection pools from being overwhelmed?
6. **Warnings:** Why does executing `my_async_func()` without an `await` emit a `RuntimeWarning: coroutine was never awaited`?
7. **Legacy Integration:** How can you execute a CPU-intensive function or legacy synchronous library without freezing the Asyncio Event Loop?
8. **Cancellation Protocol:** When an async task is cancelled, what exception is raised inside the coroutine, and what must you do if you catch it?
9. **Async Protocols:** What magic dunder methods are required to implement an asynchronous context manager (`async with`) and an asynchronous iterator (`async for`)?
10. **Async Queues:** How do you coordinate clean shutdown of worker coroutines listening to an `asyncio.Queue`?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
- **Preemptive:** The OS scheduler forcefully interrupts threads at arbitrary intervals to switch tasks.
- **Cooperative:** Coroutines voluntarily surrender execution control back to the Event Loop exclusively at explicit `await` pause points.

#### Answer 2:
The coroutine pauses its execution state, yields control back to the Event Loop, and allows the Event Loop to execute other pending coroutines until the awaited I/O operation completes.

#### Answer 3:
`time.sleep()` is a synchronous OS-level thread block that completely freezes the single thread running the Event Loop, preventing all other concurrent coroutines from making progress. Use **`await asyncio.sleep(5)`**.

#### Answer 4:
`asyncio.TaskGroup` enforces structured concurrency: If any child task raises an exception, the `TaskGroup` **automatically cancels all remaining sibling tasks** and raises an `ExceptionGroup`, preventing orphaned background tasks from leaking.

#### Answer 5:
It acts as a token bucket counter. Only $N$ tasks can enter the `async with semaphore:` block simultaneously. Subsequent tasks queue up and wait until active tasks release their token.

#### Answer 6:
Calling `async def` does not execute the function body; it merely constructs a dormant **coroutine object**. It must be scheduled via `await` or `asyncio.create_task()` to execute.

#### Answer 7:
Wrap the call with **`await asyncio.to_thread(sync_function, *args)`**, which runs the blocking work on an underlying thread pool while keeping the Event Loop unblocked.

#### Answer 8:
**`asyncio.CancelledError`** is raised. If caught for cleanup purposes, it **must be re-raised** (`raise`) so the task terminates properly.

#### Answer 9:
- Async Context Manager: `__aenter__(self)` and `__aexit__(self, exc_type, exc_val, exc_tb)`
- Async Iterator: `__aiter__(self)` and `__anext__(self)` (raising `StopAsyncIteration`)

#### Answer 10:
Send a **sentinel value** (such as `None`) into the queue for each worker task, or have the main loop call `worker_task.cancel()` after calling `await queue.join()`.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Rate-Limited Async URL Status Checker

**Goal:** Write a coroutine `check_urls(urls: list[str], max_concurrency: int = 3) -> list[dict]` that checks status codes with a rate-limiting semaphore.

<details>
<summary><b>Solution Code</b></summary>

```python
import asyncio

async def mock_ping(url: str) -> dict[str, object]:
    await asyncio.sleep(0.05)  # Simulate network ping
    return {"url": url, "status": 200, "healthy": True}

async def check_urls(urls: list[str], max_concurrency: int = 3) -> list[dict[str, object]]:
    sem = asyncio.Semaphore(max_concurrency)
    
    async def safe_fetch(url: str):
        async with sem:
            return await mock_ping(url)
            
    return await asyncio.gather(*(safe_fetch(u) for u in urls))

# Verification:
async def main():
    target_urls = [f"https://api.service.com/{i}" for i in range(1, 7)]
    results = await check_urls(target_urls, max_concurrency=2)
    print("Checked URLs count:", len(results))

asyncio.run(main())
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Blocking call inside a coroutine

```python
import asyncio, time

async def fetch(n: int) -> int:
    time.sleep(1)          # not asyncio.sleep
    return n

async def main() -> None:
    start = time.perf_counter()
    await asyncio.gather(*(fetch(i) for i in range(5)))
    print(f"{time.perf_counter() - start:.1f}s")

asyncio.run(main())
```

**Observed symptom:** Takes 5 seconds. You expected about 1.

**(a)** Why did `gather` not overlap the work?

**(b)** What is the fix for a genuinely blocking library you cannot change?

**(c)** How would you detect this class of bug automatically?

<details>
<summary><b>Show the diagnosis</b></summary>

`time.sleep` blocks the **event loop thread**. While it sleeps, no other coroutine can run — there is only one thread, and nothing yielded control. `await` is the only point at which the loop can switch.

**Fix:** `await asyncio.sleep(1)` here. For a third-party blocking library, push it off the loop: `await asyncio.to_thread(func, *args)` (or `loop.run_in_executor`). For CPU-bound work use a `ProcessPoolExecutor`.

**Detect it:** run with `asyncio.run(main(), debug=True)` or `PYTHONASYNCIODEBUG=1` — the loop logs any callback that takes longer than 100 ms. `aiodebug` and `blockbuster` do this more aggressively. In production, a rising event-loop-lag metric is the signal.

</details>

---

### D2. Coroutine never awaited

```python
import asyncio

async def save(record: dict) -> None:
    await asyncio.sleep(0.01)
    print("saved", record)

async def main() -> None:
    for i in range(3):
        save({"id": i})        # no await
    print("done")

asyncio.run(main())
```

**Observed symptom:** Prints only `done`, plus `RuntimeWarning: coroutine 'save' was never awaited`. Nothing is saved.

**(a)** What does calling an `async def` function actually return?

**(b)** Give two correct ways to run all three concurrently.

**(c)** Why is this a warning rather than an error?

<details>
<summary><b>Show the diagnosis</b></summary>

Calling a coroutine function returns a **coroutine object**; it does not start executing. Discarding it means the body never runs.

**Fix 1:** `await save(...)` in the loop — sequential. **Fix 2:** collect and gather — `await asyncio.gather(*(save({'id': i}) for i in range(3)))` — concurrent. In 3.11+ prefer `async with asyncio.TaskGroup() as tg: tg.create_task(...)`, which also cancels siblings on failure.

**Only a warning** because Python cannot know at call time whether you intend to await later; it detects the mistake at garbage collection, by which point the call site is gone. Turn it into an error in CI with `-W error::RuntimeWarning`.

</details>

---

### D3. Task exception never retrieved

```python
import asyncio

async def flaky() -> None:
    raise ValueError("failed")

async def main() -> None:
    asyncio.create_task(flaky())
    await asyncio.sleep(0.1)
    print("main finished normally")

asyncio.run(main())
```

**Observed symptom:** Prints `main finished normally`, then `Task exception was never retrieved` on stderr. Exit code is 0.

**(a)** Why did the `ValueError` not propagate?

**(b)** What are the two ways to make failures visible?

**(c)** Why is a zero exit code the dangerous part here?

<details>
<summary><b>Show the diagnosis</b></summary>

`create_task` schedules the coroutine and returns a `Task`. The exception is stored *on the task*; nobody awaited it, so nobody observed it. The event loop reports it only when the task is garbage collected.

**Fix 1:** keep a reference and await it — `task = asyncio.create_task(...)`, then `await task`. **Fix 2 (better):** `asyncio.TaskGroup`, which propagates any child failure as an `ExceptionGroup` when the block exits, and cancels the remaining siblings.

**The zero exit code** means CI passes, health checks pass, and your orchestrator believes the job succeeded. Silent failure with a success signal is worse than a crash. Also beware: a task with no strong reference can be garbage collected *mid-execution* — always keep the handle.

</details>

---

### D4. Unbounded concurrency

```python
import asyncio, httpx

async def fetch(client: httpx.AsyncClient, url: str) -> int:
    r = await client.get(url)
    return r.status_code

async def main(urls: list[str]) -> None:
    async with httpx.AsyncClient() as client:
        await asyncio.gather(*(fetch(client, u) for u in urls))
```

**Observed symptom:** With 50,000 URLs: file-descriptor exhaustion, connection resets, and the target site rate-limits or bans you.

**(a)** What did `gather` do that caused this?

**(b)** What is the idiomatic way to bound it?

**(c)** Why is a semaphore better than batching into chunks of N?

<details>
<summary><b>Show the diagnosis</b></summary>

`gather` starts **every** coroutine immediately. 50,000 concurrent connections exhausts local file descriptors and looks like an attack to the server.

**Bound it** with a semaphore:

```python
sem = asyncio.Semaphore(20)
async def bounded(u):
    async with sem:
        return await fetch(client, u)
```

**Better than chunking** because a semaphore keeps the pipeline *full*: as soon as one request finishes, the next starts. Fixed batches of N wait for the slowest member of each batch before starting the next, so one slow URL idles 19 workers. Also set `httpx.Limits(max_connections=...)` and a per-request timeout — Module 10's scraper daemon does all three.

</details>

---

### D5. Async generator not closed

```python
import asyncio

async def rows():
    conn = "opened"
    try:
        for i in range(1000):
            yield i
    finally:
        print("cleanup ran")

async def main() -> None:
    async for row in rows():
        if row > 2:
            break          # abandon the generator

asyncio.run(main())
```

**Observed symptom:** `cleanup ran` prints late, at interpreter shutdown, or sometimes not at all — and in a real version the database connection leaks.

**(a)** Why does `finally` not run at the `break`?

**(b)** What construct guarantees prompt cleanup?

**(c)** What does `asyncio.run` already do for you here, and why is it not enough?

<details>
<summary><b>Show the diagnosis</b></summary>

Breaking out of `async for` leaves the generator suspended at the `yield`. Its `finally` runs only when the generator is closed — which happens at garbage collection, at an unpredictable time, and requires a running event loop to await `aclose()`.

**Fix:** `contextlib.aclosing` —

```python
async with aclosing(rows()) as gen:
    async for row in gen:
        ...
```

This guarantees `aclose()` on exit, so cleanup is prompt and deterministic.

`asyncio.run` does call `loop.shutdown_asyncgens()` at the end, which is why the message appears *eventually*. That is not enough: the connection stayed open for the rest of the program, and in a long-lived service 'eventually' can mean hours and thousands of leaked handles.

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
