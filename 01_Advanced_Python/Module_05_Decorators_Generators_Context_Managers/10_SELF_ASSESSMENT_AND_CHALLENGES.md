# Module 05: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Decorators, Generators, and Context Managers before moving to **Module 06**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Generators vs Functions:** What is the fundamental difference in execution state between a function using `return` and a function using `yield`?
2. **Decorator Metadata:** Why should you always decorate your inner wrapper with `@functools.wraps(func)`?
3. **Memory Footprint:** Why does `(x**2 for x in range(10_000_000))` consume ~100 bytes of RAM, while `[x**2 for x in range(10_000_000)]` consumes ~400 MB?
4. **The Iterator Protocol:** What two magic methods must an object implement to satisfy Python's Iterator Protocol?
5. **Context Manager Protocol:** What are the exact arguments passed to `__exit__(self, exc_type, exc_val, exc_tb)` when an exception occurs inside a `with` block?
6. **Exception Control:** If an exception occurs inside a `with` block, how can the context manager suppress the error and prevent it from crashing the program?
7. **Delegation Syntax:** What does the `yield from iterable` syntax accomplish in Python 3.3+?
8. **Parameterized Decorators:** Why does a parameterized decorator (e.g. `@retry(max_attempts=3)`) require 3 nested function definitions instead of 2?
9. **One-Time Streams:** What happens if you attempt to iterate over an already-exhausted generator a second time in a `for` loop?
10. **Standard Library Caching:** How does `@functools.lru_cache(maxsize=128)` optimize repeated recursive function calls?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
- `return` terminates the function, destroys its local stack frame, and returns a final value.
- `yield` produces a value, pauses the function, and preserves its entire execution state (variables, instruction pointer) so it can resume on the next `next()` call.

#### Answer 2:
It copies the original function's metadata (`__name__`, `__doc__`, `__annotations__`, and `__module__`) to the wrapper, preventing debugging tools, IDE autocomplete, and test frameworks from seeing a generic `'wrapper'` function.

#### Answer 3:
The generator expression calculates values **lazily on demand** one item at a time in $O(1)$ memory. The list comprehension evaluates and stores all 10,000,000 integers in RAM immediately in $O(N)$ memory.

#### Answer 4:
1. `__iter__(self)`: Must return the iterator object itself.
2. `__next__(self)`: Must return the next value, or raise `StopIteration` when no items remain.

#### Answer 5:
- `exc_type`: The exception class (e.g. `ZeroDivisionError`).
- `exc_val`: The exception instance/message.
- `exc_tb`: The traceback object.
(If no exception occurred, all three arguments are `None`).

#### Answer 6:
`__exit__()` must return **`True`**. This signals to Python that the exception was safely handled, suppressing it from propagating.

#### Answer 7:
`yield from` transparently delegates generation to another sub-generator or iterable, forwarding all values, exceptions, and return values directly to the caller without manual `for item in subgen: yield item` loops.

#### Answer 8:
- Layer 1: Accepts decorator configuration arguments (e.g., `max_attempts`).
- Layer 2: Accepts the target function being decorated (`func`).
- Layer 3: Accepts runtime arguments (`*args, **kwargs`) passed during actual execution.

#### Answer 9:
The loop terminates immediately without executing any iterations, because the generator's internal state is exhausted and it immediately raises `StopIteration`.

#### Answer 10:
It stores the return values of previous function calls in an in-memory **Least Recently Used (LRU) dictionary**. If the function is called again with identical arguments, it returns the cached result in $O(1)$ time without re-running the computation.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: The Exponential Backoff Retry Decorator

**Goal:** Create a parameterized decorator `@retry(max_retries=3, backoff_factor=0.5)` that automatically retries a failing function with exponential backoff delays.

<details>
<summary><b>Solution Code</b></summary>

```python
import functools
import time

def retry(max_retries: int = 3, backoff_factor: float = 0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = backoff_factor
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise e
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff (0.5s, 1.0s, 2.0s...)
        return wrapper
    return decorator
```
</details>

---

### Challenge 2: Streaming Chunked Generator

**Goal:** Write a generator function `chunked_stream(data_stream, chunk_size: int)` that yields elements in batches of `chunk_size`.

<details>
<summary><b>Solution Code</b></summary>

```python
from typing import Generator, Iterable, TypeVar

T = TypeVar("T")

def chunked_stream(iterable: Iterable[T], chunk_size: int) -> Generator[list[T], None, None]:
    chunk: list[T] = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk  # Yield final partial batch

# Verification:
stream = range(1, 11)
print(list(chunked_stream(stream, 3)))
# Output: [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Decorator without functools.wraps

```python
def timed(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper

@timed
def calculate(x: int) -> int:
    """Compute the answer."""
    return x * 2

print(calculate.__name__, calculate.__doc__)
```

**Observed symptom:** Prints `wrapper None` — the function lost its identity.

**(a)** What metadata was lost?

**(b)** What is the one-line fix?

**(c)** Name two tools that break because of this.

<details>
<summary><b>Show the diagnosis</b></summary>

`__name__`, `__doc__`, `__qualname__`, `__module__`, `__annotations__` and `__dict__` all now describe the wrapper, not the wrapped function.

**Fix:** `@functools.wraps(fn)` on the wrapper. It copies all of the above and sets `__wrapped__` so introspection can find the original.

**Two tools that break:** **pytest** — a decorated test function reports as `wrapper` in output and fixture resolution can fail; and **Sphinx / any documentation generator** — every decorated function documents as "wrapper" with no docstring. Also affected: `pickle` (which looks up by qualified name), and debuggers showing the wrong frame name. Note `wraps` still does not fix the *signature* — see Module 21's diagnostic D4 for why FastAPI needs more.

</details>

---

### D2. Generator consumed twice

```python
def parse(path: str):
    for line in open(path):
        yield line.strip()

records = parse("data.txt")
print(f"count: {sum(1 for _ in records)}")
for record in records:
    print(record)
```

**Observed symptom:** The count is correct. The loop prints nothing.

**(a)** Why is the generator empty the second time?

**(b)** What are the two ways to fix it, and their trade-off?

**(c)** How would you detect this class of bug in review?

<details>
<summary><b>Show the diagnosis</b></summary>

A generator is a **one-shot iterator**. Once exhausted it stays exhausted; there is no rewind. The `sum` consumed every item.

**Two fixes:** materialise it — `records = list(parse(path))` — which allows repeated iteration at the cost of holding everything in memory; or call the generator function again — `for record in parse(path)` — which re-reads the file, using no extra memory but doing the I/O twice. The trade-off is memory versus repeated work, and which is right depends on the file size.

**Detect in review:** any variable holding a generator that appears more than once. A useful habit is naming them for their one-shot nature (`record_stream`, not `records`), and returning a `list` from public APIs unless streaming is the documented point — a caller cannot tell a generator from a list until it silently comes back empty.

</details>

---

### D3. Context manager swallowing exceptions

```python
class Transaction:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            print(f"rolling back: {exc}")
        return True

with Transaction():
    raise ValueError("constraint violated")

print("execution continues")
```

**Observed symptom:** Prints the rollback message, then `execution continues`. The `ValueError` vanishes.

**(a)** What does returning `True` from `__exit__` mean?

**(b)** What should it return here?

**(c)** When is suppressing an exception legitimate?

<details>
<summary><b>Show the diagnosis</b></summary>

A truthy return from `__exit__` tells Python the exception has been **handled** and must be suppressed. The caller never learns the transaction failed.

**It should return `False`** (or simply `None`, which is falsy) — do the rollback, then let the exception propagate so the caller can decide.

**Legitimate suppression** is rare and always deliberate: `contextlib.suppress(FileNotFoundError)` is the canonical example, and its *name* announces the intent. A manager that silently eats exceptions is one of the hardest bugs to find, because the symptom appears far downstream where the data turns out to be missing. The rule: return `False` unless the class name says 'suppress'.

</details>

---

### D4. Generator with cleanup that never runs

```python
def read_rows(path: str):
    fh = open(path)
    try:
        for line in fh:
            yield line
    finally:
        fh.close()
        print("closed")

for row in read_rows("data.txt"):
    if row.startswith("STOP"):
        break
```

**Observed symptom:** `closed` prints at an unpredictable time, and under load the process runs out of file descriptors.

**(a)** Why does `finally` not run at the `break`?

**(b)** What construct guarantees prompt cleanup?

**(c)** Why is the `try/finally` still worth keeping?

<details>
<summary><b>Show the diagnosis</b></summary>

Breaking out leaves the generator **suspended** at the `yield`. Its `finally` runs only when the generator is closed, which happens at garbage collection — unpredictably, and in a reference cycle possibly never.

**Prompt cleanup:** `contextlib.closing`:
```python
with closing(read_rows(path)) as rows:
    for row in rows:
        ...
```
This calls `.close()` on exit, which throws `GeneratorExit` into the generator and runs the `finally` immediately.

**Keep the `try/finally`** because it is what makes `close()` effective at all — without it, closing the generator would not release the file. The two work together: the `finally` defines the cleanup, and `closing` guarantees it is triggered on time. Better still, put the `with open(...)` *inside* the generator so the file is scoped to the iteration.

</details>

---

### D5. Decorator with arguments, one layer short

```python
import functools

def retry(times: int):
    @functools.wraps(times)
    def wrapper(*args, **kwargs):
        for _ in range(times):
            try:
                return times(*args, **kwargs)
            except Exception:
                continue
    return wrapper

@retry(3)
def flaky() -> str:
    return "ok"
```

**Observed symptom:** `TypeError: 'int' object is not callable`.

**(a)** How many layers does a decorator with arguments need, and how many are here?

**(b)** Write the correct structure.

**(c)** How do you write a decorator that works both with and without arguments?

<details>
<summary><b>Show the diagnosis</b></summary>

It needs **three** levels: the argument-taking factory, the decorator that receives the function, and the wrapper. This has two, so `times` is being used where the function should be.

**Correct:**
```python
def retry(times: int):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return fn(*args, **kwargs)
                except Exception:
                    if attempt == times - 1:
                        raise
        return wrapper
    return decorator
```
Note the re-raise on the final attempt — the original also returned `None` silently after exhausting retries, which is a second bug.

**Both forms:** accept the function as an optional first parameter — `def retry(fn=None, *, times=3)` — and if `fn is None`, return `functools.partial(retry, times=times)`. That is how `@dataclass` supports both `@dataclass` and `@dataclass(frozen=True)`.

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
