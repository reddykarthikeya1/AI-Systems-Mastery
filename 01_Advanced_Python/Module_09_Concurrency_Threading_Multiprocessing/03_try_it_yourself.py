"""Beginner playground for Module 09 - Concurrency: Threading & Multiprocessing.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import queue
import threading

# -------------------------------------------- 1. Thread-Safe Queues
q = queue.Queue()
q.put("task_1")
q.put("task_2")
assert q.qsize() == 2
assert q.get() == "task_1"
assert q.get() == "task_2"
assert q.empty()
print("Queue FIFO ordering verified in thread-safe buffer.")

# -------------------------------------------- 2. Concurrent Execution with ThreadPoolExecutor
def square(n):
    return n * n

with ThreadPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(square, [1, 2, 3, 4]))

assert results == [1, 4, 9, 16]
assert len(results) == 4
print(f"ThreadPool computed squares: {results}")

# -------------------------------------------- 3. Mutex Synchronization with Locks
lock = threading.Lock()
shared_counter = 0

with lock:
    shared_counter += 1

assert shared_counter == 1
assert not lock.locked()
print(f"Thread lock acquired and released; counter = {shared_counter}.")

print()
print("All checks passed.")
