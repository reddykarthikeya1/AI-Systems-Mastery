# Debug Lab Answers: Module 07

<details>
<summary>Bug 1: Platform-dependent default text encoding</summary>

### Root Cause
In Python prior to PEP 597 / Python 3.15 UTF-8 Mode, `open()` uses `locale.getpreferredencoding()`. On Windows, this is typically `cp1252`, which cannot encode arbitrary Unicode symbols.

### Fix
Always specify `encoding="utf-8"` on all file operations:
```python
with open(target, "w", encoding="utf-8") as f:
    f.write(...)
```
</details>

<details>
<summary>Bug 2: JSON keys coerced to strings</summary>

### Root Cause
The JSON specification (RFC 8259) requires all object keys to be strings. `json.dumps()` automatically stringifies integer dictionary keys, but `json.loads()` does not automatically restore their integer type.

### Fix
Re-cast keys after deserialization, or use a custom `object_hook`:
```python
deserialized = {int(k): v for k, v in json.loads(serialized).items()}
```
</details>

<details>
<summary>Bug 3: Naive vs Aware datetime comparison</summary>

### Root Cause
`datetime.fromisoformat("...")` without a UTC offset generates an offset-naive datetime. Python prevents comparing naive and timezone-aware datetimes to prevent subtle timezone bugs.

### Fix
Always use timezone-aware datetimes (e.g. `UTC`):
```python
from datetime import UTC, datetime

naive_parsed = datetime.fromisoformat("2026-09-01T12:00:00").replace(tzinfo=UTC)
```
</details>
