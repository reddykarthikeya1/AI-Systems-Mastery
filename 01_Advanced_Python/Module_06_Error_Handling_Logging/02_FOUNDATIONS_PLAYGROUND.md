# 🐣 Interactive Foundations Playground: Error Handling & Logging

> *"Professional code doesn't magically avoid errors; it plans for them and recovers gracefully."*

Welcome to Module 06! Let's learn how to catch crashes before they terminate your application.

---

## 1. The `try ... except` Shield

When dangerous code might fail (like dividing by user input or opening a missing file), wrap it in a `try` block:

```python
try:
    number = int(input("Enter a whole number: "))
    result = 100 / number
    print(f"100 divided by {number} is {result}")
except ZeroDivisionError:
    print("Oops! You cannot divide by zero.")
except ValueError:
 print("Invalid input! That was not a whole number.")
```

---

## 2. Adding `else` and `finally`

```python
try:
    f = open("data.txt", "r")
except FileNotFoundError:
    print("File not found! Starting with empty data.")
else:
    # Runs ONLY if no error occurred in try:
    print("File read successfully!")
finally:
    # Runs ALWAYS, no matter what happens (even after crashes):
    print("Cleanup step complete.")
```

---

## 3. Basic Logging in 30 Seconds

Instead of scattering temporary `print()` statements everywhere, use Python's professional `logging` module:

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

logging.info("Application initialized.")
logging.warning("Disk space running low (15% left).")
logging.error("Database connection refused!")
```

---

## 4. Run the Interactive Playground
```bash
python 03_try_it_yourself.py
```
Test a crash-proof input validator and see structured logging in the console!

---

## 5. Beginner Quick-Check Drills

### Drill 1: Catch-All Exception
What is the base exception class that catches almost all standard Python errors?
```python
try:
    something_risky()
except ___ as e:
    print(f"Caught error: {e}")
```
<details><summary><b>Show Answer</b></summary>
<b><code>Exception</code></b>
</details>

---

### Drill 2: Mandatory Cleanup
Which block in a `try-except` structure runs unconditionally whether an error occurs or not?
<details><summary><b>Show Answer</b></summary>
<b><code>finally</code></b>
</details>\n