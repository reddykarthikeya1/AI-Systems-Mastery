# Module 09: Troubleshooting, Deadlocks & Multiprocessing Traps

This reference guide details common concurrency bugs, race conditions, deadlocks, and OS-specific multiprocessing traps in Python.

---

## 1. The Windows Multiprocessing `RuntimeError` (Missing `__main__` Guard)

### The Bug
```python
import multiprocessing

def worker():
    print("Worker running")

p = multiprocessing.Process(target=worker)
p.start() # ❌ On Windows: Infinite recursive process fork crash!
```
**Crash:** `RuntimeError: An attempt has been made to start a new process before the current process has finished its bootstrapping phase.`

### Why It Happens
Unlike Linux (which uses POSIX `fork()` to clone memory), Windows spawns a brand-new Python process and re-imports the original script file. Without an `if __name__ == "__main__":` guard, the new process executes `p.start()` again, creating an infinite loop of crashing processes!

### The Fix
Always wrap top-level process spawns inside the `__main__` guard:
```python
if __name__ == "__main__":
    p = multiprocessing.Process(target=worker)
    p.start()
    p.join()
```

---

## 2. The Deadlock Trap (Circular Lock Acquisition)

### The Bug
```python
lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_1():
    with lock_a:
        time.sleep(0.01)
        with lock_b:  # Waiting for lock_b...
            print("Thread 1 finished")

def thread_2():
    with lock_b:
        time.sleep(0.01)
        with lock_a:  # Waiting for lock_a... (DEADLOCK! Neither can proceed!)
            print("Thread 2 finished")
```

### The Fix
Always acquire locks in the **exact same global order across all threads** (e.g. always acquire `lock_a` before `lock_b`).

---

## 3. Passing Unpicklable Objects to `multiprocessing`

### The Bug
```python
from concurrent.futures import ProcessPoolExecutor

def main():
    # Lambdas and local nested functions cannot be pickled!
    local_calc = lambda x: x * 2
    with ProcessPoolExecutor() as pool:
        pool.map(local_calc, [1, 2, 3])  # ❌ PicklingError: Can't pickle local object
```

### The Fix
Use top-level module functions instead of inner closures or `lambda` expressions when dispatching tasks to `ProcessPoolExecutor`.
