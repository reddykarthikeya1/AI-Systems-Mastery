# Module 06: Troubleshooting, Exception Traps & Logging Bugs

This reference guide details common errors and security hazards in error handling and logging systems.

---

## 1. The Bare `except:` & `BaseException` Trap

### The Bug
```python
while True:
    try:
        process_incoming_data()
    except:  # ❌ BARE EXCEPT!
        print("An error occurred, continuing...")
```

### Why It Happens
A bare `except:` catches **`BaseException`**, which includes `KeyboardInterrupt` (Ctrl+C) and `SystemExit`. The user cannot stop the program from the terminal!

### The Fix
Always catch `Exception` or specific error types:
```python
while True:
    try:
        process_incoming_data()
    except Exception as e:  # ✅ Allows KeyboardInterrupt and SystemExit to exit cleanly
        logger.error(f"Failed processing: {e}")
```

---

## 2. The Silent Failure Trap (`except Exception: pass`)

### The Anti-Pattern
```python
try:
    save_user_order_to_database(order)
except Exception:
    pass  # ❌ Silently swallowed! No one knows the order was lost!
```

### The Fix
Never silently swallow errors in production. Always log the error or re-raise:
```python
try:
    save_user_order_to_database(order)
except Exception as e:
    logger.exception("Failed to save user order to database!")
    raise
```

---

## 3. Forgetting `exc_info=True` in `logger.error()`

### The Bug
```python
try:
    10 / 0
except ZeroDivisionError as e:
    logger.error(f"Math error occurred: {e}")
```
**Output:** `[ERROR] Math error occurred: division by zero` *(Traceback is completely lost!)*

### The Fix
Use `logger.exception()` (or `logger.error(..., exc_info=True)`) to automatically append the full traceback:
```python
try:
    10 / 0
except ZeroDivisionError:
    logger.exception("Math error occurred during calculation")
```

---

## 4. Duplicate Log Messages (Handler Leaks)

### Why It Happens
If you call `logger.addHandler(handler)` every time a function is called, the logger accumulates multiple handlers and prints each message 2, 3, or 10 times!

### The Fix
Configure handlers **once** at module startup or application entry point:
```python
# Guard against duplicate handler registration:
if not logger.handlers:
    logger.addHandler(console_handler)
```
