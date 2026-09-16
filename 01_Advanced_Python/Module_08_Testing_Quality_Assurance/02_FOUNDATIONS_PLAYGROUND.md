# 🐣 Interactive Foundations Playground: Testing with Pytest

> *"Testing is simply writing a tiny Python script that checks if your real Python script works properly."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to Module 08! Let's demystify automated testing.

---

## 1. The `assert` Statement in 10 Seconds

An `assert` statement tests whether a condition is `True`.
- If it's `True`, Python continues silently without complaint.
- If it's `False`, Python crashes immediately with an `AssertionError`!

```python
def add(x, y):
    return x + y

# A test is just assertions:
assert add(2, 3) == 5       # Passes silently!
assert add(-1, 1) == 0      # Passes silently!
# assert add(2, 2) == 5     # ❌ Crashes with AssertionError!
print("All assertions passed!")
```

---

## 2. Writing Your First Pytest Test

In pytest:
1. Create a file named `test_math.py` (must start with `test_`).
2. Define functions named `test_...`:

```python
# test_math.py
def test_addition():
    assert 1 + 1 == 2

def test_string_uppercase():
    assert "hello".upper() == "HELLO"
```

3. Run in your terminal:
   ```bash
   pytest
   ```
4. Pytest automatically discovers your file, runs every `test_` function, and prints beautiful **green dots** for passing tests!

---

## 3. Run the Interactive Playground
```bash
python 03_try_it_yourself.py
```
Run our mini test runner and watch assertions catch deliberate bugs in real time!

---

## 4. Beginner Quick-Check Drills

### Drill 1: Test Discovery Rule
What prefix must test files and test functions have for pytest to find them automatically?
<details><summary><b>Show Answer</b></summary>
<b><code>test_</code></b> (e.g. <code>test_calculator.py</code> and <code>def test_add():</code>).
</details>

---

### Drill 2: Testing Exceptions
Which pytest context manager checks that a function properly raises a specific error?
```python
import pytest

with pytest.___(ZeroDivisionError):
    10 / 0
```
<details><summary><b>Show Answer</b></summary>
<b><code>pytest.raises(ZeroDivisionError)</code></b>
</details>\n