# 🐣 Interactive Foundations Playground: Concurrency: Threading & Multiprocessing

> *"Threads share memory for I/O; processes run isolated memory for CPU-bound computation."*

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
from concurrent.futures import ThreadPoolExecutor
import queue
import threading
```

---

## 1. Thread-Safe Queues

`queue.Queue` manages producer-consumer coordination with built-in locking.

```python
q = queue.Queue()
q.put("task_1")
q.put("task_2")
assert q.qsize() == 2
assert q.get() == "task_1"
assert q.get() == "task_2"
assert q.empty()
print("Queue FIFO ordering verified in thread-safe buffer.")
```

---

## 2. Concurrent Execution with ThreadPoolExecutor

`ThreadPoolExecutor` simplifies managing worker pools for concurrent tasks.

```python
def square(n):
    return n * n

with ThreadPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(square, [1, 2, 3, 4]))

assert results == [1, 4, 9, 16]
assert len(results) == 4
print(f"ThreadPool computed squares: {results}")
```

---

## 3. Mutex Synchronization with Locks

Locks prevent race conditions when multiple threads mutate shared resources.

```python
lock = threading.Lock()
shared_counter = 0

with lock:
    shared_counter += 1

assert shared_counter == 1
assert not lock.locked()
print(f"Thread lock acquired and released; counter = {shared_counter}.")
```

---
