# Debug Lab Answers: Module 09

<details>
<summary>Bug 1: Race condition on shared counter</summary>

### Root Cause
`shared_counter += 1` is not atomic in Python. It disassembles into `LOAD_GLOBAL`, `LOAD_CONST`, `BINARY_OP`, `STORE_GLOBAL`. If a thread switch occurs between load and store, the update is lost.

### Fix
Protect critical sections with a `threading.Lock()`:
```python
counter_lock = threading.Lock()
with counter_lock:
    shared_counter += 1
```
</details>

<details>
<summary>Bug 2: Inconsistent lock acquisition order (AB/BA Deadlock)</summary>

### Root Cause
Dijkstra's resource hierarchy condition is violated. When multiple threads acquire multiple locks in differing orders, a circular wait deadlock occurs.

### Fix
Always acquire multiple locks in a globally defined, consistent order, or use a single coarse lock:
```python
# Both threads acquire lock_a, then lock_b:
with lock_a:
    with lock_b:
        pass
```
</details>

<details>
<summary>Bug 3: Abrupt daemon thread termination</summary>

### Root Cause
When Python's main thread exits, all `daemon=True` threads are terminated instantly without running `finally:` blocks or flushing open file streams.

### Fix
Use standard non-daemon threads or coordinate shutdown with a `threading.Event()` and explicit `thread.join()`:
```python
t = threading.Thread(target=daemon_file_writer, daemon=False)
t.start()
t.join()
```
</details>
