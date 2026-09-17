# 🐣 Interactive Foundations Playground: Concurrency: Asyncio & Event Loops

> *"Asynchronous event loops multiplex thousands of concurrent I/O operations on a single thread."*

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
import asyncio
```

---

## 1. Asynchronous Coroutines & Event Loop

Coroutines yield control to the event loop using `await` without blocking system threads.

```python
async def fetch_value(val):
    return val * 10

val = asyncio.run(fetch_value(5))
assert val == 50
print(f"Async coroutine returned: {val}")
```

---

## 2. Concurrent Gathering with asyncio.gather

`asyncio.gather` fires multiple coroutines concurrently and collects results in order.

```python
async def step(n):
    await asyncio.sleep(0.001)
    return n * 2

async def run_all():
    return await asyncio.gather(step(1), step(2), step(3))

res = asyncio.run(run_all())
assert res == [2, 4, 6]
assert len(res) == 3
print(f"Gathered concurrent results: {res}")
```

---

## 3. Asynchronous Queues

`asyncio.Queue` provides non-blocking message passing between producers and consumers.

```python
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
```

---
