# Module 10: Troubleshooting, Asyncio Traps & Event Loop Freezes

This reference guide details common developer mistakes when building asynchronous architectures with Asyncio.

---

## 1. Freezing the Event Loop with `time.sleep()`

### The Bug
```python
async def handle_request():
    time.sleep(5)  # ❌ CATASTROPHIC! Freezes the ENTIRE event loop for 5 seconds!
    return "Done"
```

### Why It Happens
Asyncio relies on **cooperative multitasking** in a single OS thread. `time.sleep()` blocks the entire operating system thread, preventing all other 1,000 tasks on the event loop from running!

### The Fix
1. Use **`await asyncio.sleep(5)`** for asynchronous waits.
2. If calling a legacy blocking function (like `requests.get()`), wrap it with **`await asyncio.to_thread(legacy_fn)`**.

---

## 2. `RuntimeWarning: coroutine was never awaited`

### The Bug
```python
async def send_email(to):
    print("Email sent")

async def main():
    send_email("alice@example.com")  # ❌ Forgot 'await'! Email is NEVER sent!
```
**Warning:** `RuntimeWarning: coroutine 'send_email' was never awaited`

### Why It Happens
Calling an `async def` function does **not** execute its body immediately; it returns a **coroutine object**. The coroutine only runs when you `await` it or schedule it as a task.

### The Fix
Always `await` coroutines:
```python
await send_email("alice@example.com")
```

---

## 3. Swallowing `asyncio.CancelledError`

### The Bug
```python
async def worker():
    try:
        await long_running_task()
    except Exception:
        print("Caught error")
```

### Why It Happens
In Python 3.8+, `asyncio.CancelledError` inherits from `BaseException` rather than `Exception`, so `except Exception:` does not catch cancellation. However, if you catch `BaseException` or `CancelledError` without re-raising, the task **refuses to cancel**, causing memory leaks!

### The Fix
If you catch `CancelledError` to perform cleanup, **always re-raise it**:
```python
try:
    await long_running_task()
except asyncio.CancelledError:
    cleanup_resources()
    raise  # ✅ Propagates cancellation cleanly!
```
