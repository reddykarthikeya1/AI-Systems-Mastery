# Debug Lab Answers: Module 20

<details>
<summary>Bug 1: Using wall clock (time.time()) instead of monotonic clock</summary>

### Root Cause
`time.time()` measures calendar wall-clock time and can jump backward or forward during NTP synchronization.

### Fix
Always use `time.monotonic()` for intervals and timeouts:
```python
expires_at = time.monotonic() + ttl_seconds
```
</details>

<details>
<summary>Bug 2: None as cache miss sentinel</summary>

### Root Cause
`None` is a valid cacheable value (e.g., negative caching missing records). Returning `None` conflates "not in cache" with "cached value is None".

### Fix
Use a dedicated sentinel object:
```python
_MISSING = object()

def get(self, key: str) -> object:
    if key not in self._cache:
        return _MISSING
    val, expires_at = self._cache[key]
    if time.monotonic() > expires_at:
        del self._cache[key]
        return _MISSING
    return val
```
</details>
