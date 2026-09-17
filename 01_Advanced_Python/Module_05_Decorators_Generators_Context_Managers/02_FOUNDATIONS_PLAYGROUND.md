# 🐣 Interactive Foundations Playground: Decorators, Generators & Context Managers

> *"Decorators wrap execution, generators stream values, and context managers guarantee cleanup."*

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
from contextlib import contextmanager
import functools
```

---

## 1. Function Decorators Preserving Metadata

`functools.wraps` ensures wrapped functions retain their original name and docstring.

```python
call_log = []
def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        call_log.append(func.__name__)
        return func(*args, **kwargs)
    return wrapper

@trace
def greet(name):
    """Greeting function docstring."""
    return f"Hello, {name}!"

res = greet("Pythonista")
assert res == "Hello, Pythonista!"
assert greet.__name__ == "greet"
assert call_log == ["greet"]
print(f"Decorated function executed: {res}")
```

---

## 2. Stateful Generators with Yield

Generators pause execution state and resume upon `next()`, providing constant memory streams.

```python
def fibonacci(limit):
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

fibs = list(fibonacci(7))
assert fibs == [0, 1, 1, 2, 3, 5, 8]
assert len(fibs) == 7
print(f"Generated first 7 Fibonacci numbers: {fibs}")
```

---

## 3. Deterministic Resource Management

Context managers guarantee resource cleanup even if exceptions occur during execution.

```python
cleanup_done = False
@contextmanager
def temporary_resource():
    global cleanup_done
    try:
        yield "resource_handle"
    finally:
        cleanup_done = True

with temporary_resource() as handle:
    assert handle == "resource_handle"
    assert not cleanup_done

assert cleanup_done
print("Context manager cleanup executed deterministically.")
```

---
