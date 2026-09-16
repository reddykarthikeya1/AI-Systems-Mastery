# Debug Lab Answers: Module 06

<details>
<summary>Bug 1: Accumulating duplicate log handlers</summary>

### Root Cause
`logger.addHandler()` appends a handler each time it is called. If called multiple times, the logger has multiple stream handlers attached, printing every message multiple times.

### Fix
Check `logger.hasHandlers()` or use `logging.basicConfig()` once at application startup:
```python
def setup_checkout_logger():
    logger = logging.getLogger("checkout")
    if not logger.handlers:
        handler = logging.StreamHandler()
        logger.addHandler(handler)
    return logger
```
</details>

<details>
<summary>Bug 2: Bare except: catching BaseException</summary>

### Root Cause
`except:` catches `BaseException`, which includes `KeyboardInterrupt`, `SystemExit`, and `GeneratorExit`. This traps process termination signals.

### Fix
Always catch `Exception` instead of bare `except:`:
```python
except Exception as exc:
    logger.warning("Payment processing failed: %s", exc)
```
</details>

<details>
<summary>Bug 3: Raising new exception without explicit chaining</summary>

### Root Cause
Raising `raise RuntimeError(...)` inside an except block without `from err` fails to set `__cause__` explicitly, which obscures the original root cause during debugging.

### Fix
Use explicit exception chaining with `from`:
```python
try:
    int("invalid_amount")
except ValueError as err:
    raise RuntimeError("Payment gateway processing failed") from err
```
</details>
