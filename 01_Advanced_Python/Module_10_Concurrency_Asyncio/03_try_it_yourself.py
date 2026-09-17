"""Beginner playground for Module 10 - Concurrency: Asyncio & Event Loops.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import asyncio

# -------------------------------------------- 1. Asynchronous Coroutines & Event Loop
async def fetch_value(val):
    return val * 10

val = asyncio.run(fetch_value(5))
assert val == 50
print(f"Async coroutine returned: {val}")

# -------------------------------------------- 2. Concurrent Gathering with asyncio.gather
async def step(n):
    await asyncio.sleep(0.001)
    return n * 2

async def run_all():
    return await asyncio.gather(step(1), step(2), step(3))

res = asyncio.run(run_all())
assert res == [2, 4, 6]
assert len(res) == 3
print(f"Gathered concurrent results: {res}")

# -------------------------------------------- 3. Asynchronous Queues
async def queue_demo():
    q = asyncio.Queue()
    await q.put("event_A")
    await q.put("event_B")
    first = await q.get()
    second = await q.get()
    return first, second

a, b = asyncio.run(queue_demo())
assert a == "event_A"
assert b == "event_B"
print(f"Async queue processed: {a}, {b}")

print()
print("All checks passed.")
