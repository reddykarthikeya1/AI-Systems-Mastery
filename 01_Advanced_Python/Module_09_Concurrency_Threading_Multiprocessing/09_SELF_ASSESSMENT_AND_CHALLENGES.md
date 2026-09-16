# Module 09: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Threading, Multiprocessing, the GIL, and Concurrency before moving to **Module 10**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Workload Classification:** Give two real-world examples of an I/O-bound task and two examples of a CPU-bound task in backend engineering.
2. **The GIL:** What is the Global Interpreter Lock (GIL) in CPython, and why does it prevent multiple threads from executing pure CPU calculations simultaneously?
3. **I/O Concurrency:** If the GIL exists, why does `ThreadPoolExecutor` still speed up downloading 50 web pages by 10x?
4. **Race Conditions:** What is a Race Condition, and what code construct is used to protect shared mutable state in multi-threaded programs?
5. **Memory Model:** What is the fundamental difference in computer memory architecture between Python Threads and Python Processes?
6. **Operating System Nuances:** Why will Python multiprocessing crash with an infinite spawning loop on Windows if you do not use `if __name__ == "__main__":`?
7. **Deadlock Conditions:** What is a Deadlock, and what simple design rule guarantees deadlock prevention when multiple locks are needed?
8. **Thread-Safe Queues:** What do `queue.task_done()` and `queue.join()` do in Python's standard `queue.Queue`?
9. **Process Pickling:** Why must functions passed to `ProcessPoolExecutor.map()` be picklable, top-level module functions?
10. **Modern Python 3.13:** What major concurrency milestone was introduced in Python 3.13 regarding the GIL?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
- **I/O-Bound:** Fetching data from an HTTP REST API; writing large files to an SSD.
- **CPU-Bound:** Image compression / resizing; cryptographic hashing / mathematical matrix operations.

#### Answer 2:
The GIL is a mutex that prevents multiple native OS threads from executing CPython bytecode at the same time, protecting Python's internal memory management (reference counts) from corruption.

#### Answer 3:
Whenever a thread executes an I/O operation (like waiting on network socket responses or disk reads), it **releases the GIL**, allowing other threads to run concurrently while the first thread waits.

#### Answer 4:
A race condition occurs when two or more threads access and mutate shared data concurrently, causing non-deterministic data loss. It is resolved using **`threading.Lock`** (or `threading.RLock`) to create a mutually exclusive critical section.

#### Answer 5:
- **Threads** share the exact same process memory (RAM), heap variables, and address space.
- **Processes** have completely isolated, private memory spaces, requiring explicit Inter-Process Communication (IPC) mechanisms (like queues or pipes) to share data.

#### Answer 6:
Windows does not support POSIX `fork()`; it launches a fresh Python interpreter process that re-imports the main script. Without `if __name__ == "__main__":`, every child process re-executes the process-spawning code endlessly.

#### Answer 7:
A deadlock is a standstill where two or more threads are permanently blocked because each holds a lock the other needs. Prevent it by **enforcing a global, strict lock acquisition order** across all threads.

#### Answer 8:
- `task_done()` signals to the queue that a previously retrieved task has finished processing.
- `join()` blocks the main thread until every item added to the queue has had `task_done()` called.

#### Answer 9:
Because processes have separate memory, data and function signatures must be serialized into bytes (via `pickle`) and sent across OS IPC pipes to the child process. Anonymous `lambda` functions and local closures cannot be serialized by `pickle`.

#### Answer 10:
Python 3.13 added experimental **free-threaded builds (`--disable-gil`)**, which remove the Global Interpreter Lock and allow native Python threads to execute in true multi-core parallel fashion.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Thread-Safe Metric Counter

**Goal:** Implement a thread-safe `MetricsCollector` class that counts events across multiple threads without data loss.

<details>
<summary><b>Solution Code</b></summary>

```python
import threading
from collections import defaultdict

class MetricsCollector:
    def __init__(self) -> None:
        self._counts: defaultdict[str, int] = defaultdict(int)
        self._lock = threading.Lock()

    def record_event(self, event_name: str, count: int = 1) -> None:
        with self._lock:
            self._counts[event_name] += count

    def get_count(self, event_name: str) -> int:
        with self._lock:
            return self._counts[event_name]

# Verification:
collector = MetricsCollector()
threads = [
    threading.Thread(target=lambda: [collector.record_event("http_requests") for _ in range(1000)])
    for _ in range(10)
]
for t in threads: t.start()
for t in threads: t.join()

print("Total HTTP requests recorded (Expected 10,000):", collector.get_count("http_requests"))
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Unlocked shared counter

```python
import threading

counter = 0

def increment() -> None:
    global counter
    for _ in range(100_000):
        counter += 1

threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(counter)
```

**Observed symptom:** Prints something less than 400000, and a different number each run.

**(a)** The GIL exists — so why is this still a race?

**(b)** Give two fixes and state the cost of each.

**(c)** Would this be safe on a free-threaded (PEP 703) build?

<details>
<summary><b>Show the diagnosis</b></summary>

`counter += 1` is **not atomic**. It compiles to LOAD, ADD, STORE (check with `dis.dis`), and the interpreter can switch threads between those bytecodes. The GIL guarantees only that one bytecode runs at a time, never that a *statement* is indivisible.

**Fix 1:** a `threading.Lock` around the update — correct, costs contention. **Fix 2:** `itertools.count()` or per-thread accumulators summed at the end — no lock, better scaling, more code.

**Free-threaded build:** *less* safe, not more. Removing the GIL removes the accidental protection of coarse bytecode granularity, so unsynchronised code that happened to work now fails more often. Correct locking is required either way.

</details>

---

### D2. Deadlock from lock ordering

```python
import threading, time

lock_a, lock_b = threading.Lock(), threading.Lock()

def task_one() -> None:
    with lock_a:
        time.sleep(0.01)
        with lock_b:
            pass

def task_two() -> None:
    with lock_b:
        time.sleep(0.01)
        with lock_a:
            pass

t1 = threading.Thread(target=task_one); t2 = threading.Thread(target=task_two)
t1.start(); t2.start(); t1.join(); t2.join()
```

**Observed symptom:** The program hangs forever. Both threads are alive but idle.

**(a)** Draw the wait-for cycle. Which thread holds what, and wants what?

**(b)** What is the standard prevention rule?

**(c)** Why does removing the `sleep` calls often make the bug *disappear*?

<details>
<summary><b>Show the diagnosis</b></summary>

`task_one` holds `lock_a` and waits for `lock_b`; `task_two` holds `lock_b` and waits for `lock_a`. A cycle in the wait-for graph, so neither can proceed.

**Prevention:** impose a **global lock ordering** — every code path acquires locks in the same fixed order (say, always `a` before `b`). Alternatively use `acquire(timeout=...)` and back off, or restructure so only one lock is needed.

**Removing the sleeps** makes each critical section so short that one thread usually finishes before the other starts. The bug becomes rare, not absent — the worst possible state, because it will surface in production under load. The sleeps here are a deterministic reproduction of a real timing bug.

</details>

---

### D3. ProcessPool cannot pickle the worker

```python
from concurrent.futures import ProcessPoolExecutor

def run() -> list[int]:
    def square(n: int) -> int:      # defined inside run()
        return n * n
    with ProcessPoolExecutor() as ex:
        return list(ex.map(square, range(4)))

print(run())
```

**Observed symptom:** On Windows/macOS: `AttributeError: Can't pickle local object 'run.<locals>.square'`.

**(a)** Why must the worker be picklable at all?

**(b)** What are the three ways to make this work?

**(c)** Why does the same code sometimes succeed on Linux?

<details>
<summary><b>Show the diagnosis</b></summary>

`ProcessPoolExecutor` sends the callable to a separate OS process. With the **spawn** start method (default on Windows, and macOS since 3.8) the callable is pickled **by qualified name** and re-imported in the child. A closure or a nested function has no importable name.

**Three fixes:** (1) move `square` to module level — the normal answer; (2) use `functools.partial` over a module-level function; (3) switch to `ThreadPoolExecutor` if the work is actually I/O-bound.

**On Linux** the default was historically **fork**, which copies the parent's memory wholesale, so the child already has the closure and no pickling is needed. Code that works on your Linux CI and fails on a colleague's Mac is almost always this. The Module 09 notebook demonstrates the fix with `nb_workers.py`.

</details>

---

### D4. Daemon thread killed mid-write

```python
import threading, time

def writer() -> None:
    with open("out.txt", "w") as fh:
        for i in range(100_000):
            fh.write(f"line {i}\n")

t = threading.Thread(target=writer, daemon=True)
t.start()
time.sleep(0.01)
print("main done")
```

**Observed symptom:** `out.txt` is truncated mid-line, or empty, and no error is reported.

**(a)** What does `daemon=True` actually change?

**(b)** Why is the file truncated rather than merely short?

**(c)** What is the correct pattern for background work that must finish?

<details>
<summary><b>Show the diagnosis</b></summary>

A daemon thread does not keep the interpreter alive. When the main thread exits, daemon threads are killed **abruptly** — no exception, no `finally`, no context manager `__exit__`.

**Truncated, not short:** the file object's buffer is never flushed and `close()` never runs, so whatever sat in the 8 KB buffer is lost — often mid-line.

**Correct pattern:** non-daemon thread plus an explicit `t.join()`, or a `threading.Event` for cooperative shutdown that the worker checks and responds to by cleaning up. Use daemon threads only for work that is genuinely safe to abandon, such as a metrics poller.

</details>

---

### D5. Threads for CPU work

```python
import threading, time, math

def cpu() -> None:
    sum(math.sqrt(i) for i in range(3_000_000))

start = time.perf_counter()
cpu(); cpu()
print(f"sequential: {time.perf_counter() - start:.2f}s")

start = time.perf_counter()
ts = [threading.Thread(target=cpu) for _ in range(2)]
for t in ts: t.start()
for t in ts: t.join()
print(f"threaded:   {time.perf_counter() - start:.2f}s")
```

**Observed symptom:** Threaded is the same speed or slightly *slower* than sequential, on a multi-core machine.

**(a)** Why is there no speedup?

**(b)** What would you change to get real parallelism, and what does that cost?

**(c)** How would you decide, before writing code, which of the two to reach for?

<details>
<summary><b>Show the diagnosis</b></summary>

The work is pure CPU, so it holds the GIL throughout. Only one thread executes bytecode at a time; the extra threads add context-switching overhead and nothing else.

**For real parallelism:** `ProcessPoolExecutor` — each process has its own interpreter and its own GIL. The cost is process startup (~50 ms), and every argument and result must be pickled, so it only pays off when the work per task clearly exceeds that overhead. A native extension that releases the GIL is the other route (Module 22 measures 3.21× thread scaling from Rust).

**Decide up front:** if the thread would spend its time *waiting* (network, disk, subprocess), use threads or `asyncio` — waiting releases the GIL. If it would spend its time *computing*, use processes. That one question settles it.

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
