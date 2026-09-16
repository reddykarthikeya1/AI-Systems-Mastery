# Module 06: Self-Assessment Quiz & Mastery Challenges

Test your understanding of enterprise error handling, exception hierarchies, and structured logging before moving to **Module 07**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Root Exceptions:** Why does Python have both `BaseException` and `Exception`, and why should application code only catch `Exception`?
2. **Control Flow:** What is the difference in execution conditions between the `else` block and the `finally` block in a `try/except/else/finally` statement?
3. **Exception Chaining:** When raising a high-level domain error, what does `raise ServiceError(...) from original_error` accomplish?
4. **Hiding Internal Details:** How can you explicitly suppress the root cause traceback when raising an error to avoid leaking internal system details?
5. **Python 3.11 Features:** What problem does `ExceptionGroup` and the `except*` syntax solve in concurrent/asynchronous applications?
6. **Logging Levels:** What are the 5 standard logging levels in Python, listed in order of increasing severity from lowest to highest?
7. **Traceback Logging:** What is the difference between calling `logger.error("Error occurred")` and `logger.exception("Error occurred")` inside an `except` block?
8. **File Management:** How does `RotatingFileHandler` prevent production server disks from filling up with log files?
9. **Observability:** Why do modern cloud systems (like AWS, Datadog, ELK) prefer structured JSON logs over plain unstructured text logs?
10. **Handler Architecture:** Why can calling `logger.addHandler(...)` inside a frequently-executed function cause duplicate log outputs?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
`BaseException` is the parent of special system-exiting signals like `KeyboardInterrupt` and `SystemExit`. `Exception` is the parent of standard application errors. Catching `Exception` handles bugs safely without preventing user aborts (Ctrl+C).

#### Answer 2:
- `else` executes **only if NO exceptions occurred** in the `try` block.
- `finally` executes **unconditionally**, regardless of whether an exception occurred, was handled, or remained unhandled.

#### Answer 3:
It explicitly sets `__cause__` on the new exception, preserving the original error and displaying a clean `"The above exception was the direct cause of the following exception:"` chain in the traceback.

#### Answer 4:
Use `raise ServiceError(...) from None`. Setting `from None` sets `__suppress_context__ = True`, hiding internal tracebacks from end-users.

#### Answer 5:
It allows catching and handling **multiple independent exceptions** that occur simultaneously across concurrent tasks or background worker threads.

#### Answer 6:
`DEBUG` (10) $\rightarrow$ `INFO` (20) $\rightarrow$ `WARNING` (30) $\rightarrow$ `ERROR` (40) $\rightarrow$ `CRITICAL` (50).

#### Answer 7:
`logger.exception()` automatically includes the full exception traceback (`exc_info=True`) in the log output, whereas standard `logger.error()` only outputs the message string.

#### Answer 8:
It monitors file size (`maxBytes`) and automatically closes, renames, and archives older logs up to a fixed count (`backupCount`), deleting the oldest backup to keep total disk usage strictly bounded.

#### Answer 9:
JSON logs are machine-parseable, allowing log aggregators to automatically index, filter, query, and alert on specific fields (e.g. `trace_id`, `user_id`, `status_code`) across thousands of servers.

#### Answer 10:
Loggers retain registered handlers in memory. Registering handlers repeatedly appends new handler instances to the logger's handler list, causing every subsequent log message to be emitted once per registered handler.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Custom Error Hierarchy with HTTP Mapping

**Goal:** Create a domain error hierarchy where each custom exception has an associated `http_status` code attribute.

<details>
<summary><b>Solution Code</b></summary>

```python
class APIError(Exception):
    http_status: int = 500
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

class ResourceNotFoundError(APIError):
    http_status = 404

class UnauthorizedAccessError(APIError):
    http_status = 401

class InvalidPayloadError(APIError):
    http_status = 422

# Error dispatch simulation:
def handle_error(err: APIError) -> dict[str, object]:
    return {
        "status_code": err.http_status,
        "error_type": type(err).__name__,
        "detail": err.message,
    }

print(handle_error(ResourceNotFoundError("User #102 not found")))
# Output: {'status_code': 404, 'error_type': 'ResourceNotFoundError', 'detail': 'User #102 not found'}
```
</details>

---

### Challenge 2: Contextual Logger Adapter

**Goal:** Create a `ContextAdapter` using `logging.LoggerAdapter` that automatically injects a `session_id` and `user_id` into every log record.

<details>
<summary><b>Solution Code</b></summary>

```python
import logging

class ContextAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        context = f"[User: {self.extra.get('user_id', 'Anon')} | Session: {self.extra.get('session_id', 'N/A')}]"
        return f"{context} {msg}", kwargs

# Verification:
base_logger = logging.getLogger("auth_service")
base_logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
base_logger.handlers = [console]

adapter = ContextAdapter(base_logger, {"user_id": "alice_99", "session_id": "sess_abc123"})
adapter.info("Password successfully updated.")
# Output: INFO - [User: alice_99 | Session: sess_abc123] Password successfully updated.
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Bare except swallows the interrupt

```python
import time

def poll() -> None:
    while True:
        try:
            time.sleep(1)
            raise ConnectionError("upstream down")
        except:                      # noqa: E722
            print("retrying...")
```

**Observed symptom:** Ctrl+C does not stop the program.

**(a)** Why does Ctrl+C fail to terminate it?

**(b)** What is the minimal correct change?

**(c)** Which two other exceptions does a bare `except` catch that you almost never want?

<details>
<summary><b>Show the diagnosis</b></summary>

`except:` catches **`BaseException`**, which includes `KeyboardInterrupt`. Your handler prints 'retrying' and loops, so the interrupt is discarded.

**Fix:** `except Exception:` — or better, `except ConnectionError:`, naming what you actually expect.

**Also caught:** `SystemExit` (so `sys.exit()` stops working) and `GeneratorExit` (breaking generator cleanup). The rule: catch the narrowest exception that you can actually handle, and let everything else propagate.

</details>

---

### D2. Duplicate log lines

```python
import logging

def get_logger() -> logging.Logger:
    logger = logging.getLogger("app")
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

for _ in range(3):
    get_logger().info("processing")
```

**Observed symptom:** The first message prints once, the second twice, the third three times.

**(a)** Why does the output multiply?

**(b)** Give two different fixes.

**(c)** What does `logger.propagate = False` change, and when is it the wrong fix?

<details>
<summary><b>Show the diagnosis</b></summary>

`logging.getLogger('app')` returns the **same** logger object every time — loggers are cached by name. Each call appends *another* handler, so the record is emitted once per handler.

**Fix 1:** configure logging once at application start (`logging.basicConfig` or `dictConfig`) and only ever *get* loggers afterwards. **Fix 2:** guard with `if not logger.handlers:` before adding.

`propagate = False` stops records reaching ancestor loggers. It fixes duplication caused by a handler on both the child *and* the root, but here the duplicate handlers are on the same logger, so it changes nothing. It is also a common over-correction that silently hides records from your central handler.

</details>

---

### D3. Lost exception context

```python
def load_config(path: str) -> dict:
    try:
        import json
        return json.loads(open(path).read())
    except Exception:
        raise ValueError("bad config")
```

**Observed symptom:** The traceback says only `ValueError: bad config` — you cannot tell whether the file was missing, unreadable, or malformed JSON.

**(a)** What information was destroyed, and by what exactly?

**(b)** What two syntaxes preserve the cause, and how do they differ?

**(c)** When is discarding the original deliberately correct?

<details>
<summary><b>Show the diagnosis</b></summary>

Raising a new exception inside an `except` block does keep `__context__` implicitly, but the *message* discards the useful detail, and any `from None` would drop the chain entirely. The reader loses the filename and the original error type.

**`raise ValueError('bad config') from exc`** sets `__cause__` — 'this was *caused by* that', printed as 'The above exception was the direct cause'. **Implicit chaining** (plain `raise`) sets `__context__` — 'this happened *while* handling that'. Prefer explicit `from exc`.

**Discard deliberately** only at a trust boundary — e.g. an API handler that must not leak internal paths to a client. There you use `from None`, and you log the original before dropping it.

</details>

---

### D4. `finally` swallows the return value

```python
def risky() -> int:
    try:
        raise RuntimeError("boom")
    finally:
        return 0

print(risky())
```

**Observed symptom:** Prints `0`. The `RuntimeError` disappears entirely.

**(a)** Why is the exception discarded?

**(b)** What is the rule this illustrates?

**(c)** What does a `return` inside `except` do to an exception raised in `try`?

<details>
<summary><b>Show the diagnosis</b></summary>

A `return` (or `break`, or `continue`) in a `finally` block **replaces** whatever was in flight — including an in-flight exception. The exception is discarded, not logged, not chained.

**Rule:** `finally` is for cleanup only. Never return, break, or continue from it.

**`return` in `except`** is different and legitimate: it handles the exception and returns a value. The danger is specifically `finally`, because it runs on *both* the success and failure paths, so the override is invisible when you read only the happy path.

</details>

---

### D5. Exception group from concurrent tasks

```python
import asyncio

async def worker(n: int) -> int:
    if n == 2:
        raise ValueError("two is bad")
    if n == 3:
        raise KeyError("three is worse")
    return n

async def main() -> None:
    try:
        async with asyncio.TaskGroup() as tg:
            for i in range(4):
                tg.create_task(worker(i))
    except ValueError as exc:
        print("caught:", exc)

asyncio.run(main())
```

**Observed symptom:** `ExceptionGroup` propagates uncaught — the `except ValueError` never fires.

**(a)** Why does `except ValueError` not match?

**(b)** What syntax handles this correctly?

**(c)** What happens to the `KeyError` if you only handle `ValueError`?

<details>
<summary><b>Show the diagnosis</b></summary>

`TaskGroup` collects every failure into a single **`ExceptionGroup`**, which is not a `ValueError`, so a plain `except ValueError` does not match it.

**Fix:** `except* ValueError as eg:` — the `except*` syntax (PEP 654, Python 3.11+) matches *inside* the group and binds a sub-group containing only the matching exceptions.

**The `KeyError`** is re-raised in a residual `ExceptionGroup` after your handler runs. That is the point: `except*` cannot accidentally swallow failures it did not address, unlike a broad `except Exception`.

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
