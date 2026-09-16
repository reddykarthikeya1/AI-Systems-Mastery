# Debug Lab Answers: Module 10

<details>
<summary>Bug 1: Synchronous blocking call inside coroutine</summary>

### Root Cause
`asyncio` operates on cooperative multitasking. When `time.sleep()` is called, control is never yielded back to the event loop, freezing all other pending tasks.

### Fix
Use `await asyncio.sleep(...)` or `asyncio.to_thread(...)` for CPU/blocking calls:
```python
async def fetch_url(url: str) -> str:
    await asyncio.sleep(0.5)
    return f"Content of {url}"
```
</details>

<details>
<summary>Bug 2: Coroutine called without await</summary>

### Root Cause
Calling an `async def` function returns a coroutine object. It does not begin execution until it is `await`ed or scheduled on the event loop via `asyncio.create_task()`.

### Fix
Add the missing `await`:
```python
task = await fetch_url("https://example.com")
```
</details>

<details>
<summary>Bug 3: Unretrieved task exception</summary>

### Root Cause
Exceptions inside background tasks created via `create_task()` are stored on the `Task` object. If `task.exception()` or `await task` is never called, the exception goes unhandled.

### Fix
Add a done-callback or await the task with error handling:
```python
def handle_done(task: asyncio.Task):
    if not task.cancelled() and task.exception():
        logger.error("Background task failed: %s", task.exception())

bg.add_done_callback(handle_done)
```
</details>
