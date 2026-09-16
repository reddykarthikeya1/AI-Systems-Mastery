# Debug Lab Answers: Module 05

<details>
<summary>Bug 1: Missing functools.wraps</summary>

### Root Cause
A custom decorator replaces the decorated function with `wrapper`. Without `functools.wraps(func)`, metadata (`__name__`, `__doc__`, `__annotations__`) is replaced by the wrapper's metadata.

### Fix
Decorate the inner wrapper with `@functools.wraps(func)`:
```python
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ...
        return func(*args, **kwargs)
    return wrapper
```
</details>

<details>
<summary>Bug 2: Generator exhaustion</summary>

### Root Cause
Generators produce values on demand and maintain internal state (`gi_frame`). Once exhausted (`StopIteration`), they cannot be re-iterated.

### Fix
Either convert to a list upfront if memory permits, or pass an iterable/factory that creates a fresh generator per pass:
```python
def process_stream(stream_factory):
    count1 = sum(1 for _ in stream_factory())
    count2 = sum(1 for _ in stream_factory())
```
</details>

<details>
<summary>Bug 3: Context manager __exit__ returning True</summary>

### Root Cause
In Python's context management protocol, if `__exit__` returns a truthy value, Python suppresses the exception that occurred inside the `with` block.

### Fix
Only return `True` for specifically handled exception types; return `False` (or `None`) by default:
```python
def __exit__(self, exc_type, exc_val, exc_tb):
    print("[DB] Transaction closed")
    if exc_type is not None and issubclass(exc_type, IgnorableWarning):
        return True
    return False
```
</details>
