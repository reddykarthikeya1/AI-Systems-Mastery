# Interactive Foundations Playground: Threading, Multiprocessing & The GIL

> *"Threads share the same kitchen; Processes have separate restaurants."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to the **Module 09 Concurrency Threading Multiprocessing** Playground! Here we demystify advanced concepts into bite-sized, runnable mental models.

---

## 1. Core Concept in 30 Seconds

Concurrency allows your program to juggle multiple jobs. If your script waits for downloads (I/O-bound), use **Threads**. If your script performs heavy math using CPU cores (CPU-bound), use **Processes**.

---

## 2. Micro-Code Example (3-5 Lines)

```python
import threading
import time

def boil_kettle():
    print("[*] Heating water...")
    time.sleep(1)
    print("[*] Kettle ready!")

# Run boiling water in background thread
t = threading.Thread(target=boil_kettle)
t.start()
print("[*] Buttering bread while water boils...")
t.join()  # Wait for kettle to finish
print("[*] Tea time!")
```

### Line-by-Line Breakdown:
- `threading.Thread(target=boil_kettle)`: Assigns a worker thread to execute the function in the background.
- `t.start()`: Begins execution immediately without freezing the main program.
- `t.join()`: Pauses the main program until the worker thread finishes.
- **The GIL (Global Interpreter Lock):** Python's safety lock that prevents multiple threads from running Python bytecode simultaneously, making `multiprocessing` the right choice for CPU-bound tasks.

---

## 3. Run the Interactive Playground

Execute the standalone, zero-dependency sandbox in your terminal:
```bash
python 03_try_it_yourself.py
```

---

## 4. Beginner Quick-Check Drills

### Drill 1: Quick Check
What method must you call to start a thread?

<details><summary><b>Show Answer</b></summary>

Calling `thread.start()`. Calling `thread.run()` directly runs synchronously on the main thread!
</details>

---

### Drill 2: Quick Check
What happens if you omit `thread.join()`?

<details><summary><b>Show Answer</b></summary>

The main program continues without waiting for the background thread to finish.
</details>

---
