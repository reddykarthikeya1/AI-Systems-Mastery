# 🐛 Global Debugging Playbook: Decoding Python Tracebacks into Plain English

> *"Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it."* — Brian Kernighan

When your code crashes with a red block of text, **do not panic**. That output is a **Traceback**—Python's detailed GPS map showing you the exact file, line number, and logical reason for the failure.

This playbook teaches you how to read tracebacks effortlessly and decodes the **Top 10 Python Errors** into plain, human-friendly English.

---

## 🧭 The Golden Rule: Always Read Tracebacks from the Bottom Up!

Beginners often make the mistake of reading a traceback starting from the top. **Always start at the very last line**:

```text
Traceback (most recent call last):
  File "app.py", line 42, in process_transaction
    final_amount = calculate_discount(price, coupon)
  File "calculator.py", line 18, in calculate_discount
    return price * (1 - coupon.rate)
AttributeError: 'NoneType' object has no attribute 'rate'  <─── 1. START HERE! (The Error Type & Explanation)
                                                            <─── 2. LOOK UP ONE STEP! (File name & line where it happened)
```

1. **The Bottom Line:** Tells you **WHAT** went wrong (`AttributeError: 'NoneType' object has no attribute 'rate'`).
2. **The Line Above It:** Tells you **WHERE** it happened (`File "calculator.py", line 18`).
3. **The Preceding Lines (The Call Stack):** Tells you **HOW** the program got there (who called who).

---

## 🔍 The Top 10 Python Errors Decoded

### 1. `SyntaxError: invalid syntax`
* **What it means in human terms:** You violated Python's grammar rules. Python couldn't even start running your script because a symbol is missing or misplaced.
* **Most common causes:** Forgetting a colon `:` at the end of `def`, `if`, `for`, `while`, or mismatched parentheses `()`.
* **Side-by-Side Fix:**
  ```python
  # ❌ BROKEN: Missing colon
  if score > 50
      print("Passed")

  # ✅ FIXED: Added colon
  if score > 50:
      print("Passed")
  ```

---

### 2. `IndentationError: unexpected indent` (or `unindent does not match...`)
* **What it means in human terms:** Python uses whitespace indentation instead of curly braces `{}` to define code blocks. You have inconsistent spaces or tabs.
* **Most common causes:** Mixing 4 spaces with Tabs, or indenting a line without an `if`/`for`/`def` statement above it.
* **Side-by-Side Fix:**
  ```python
  # ❌ BROKEN: Indented without a block statement
  x = 10
      y = 20

  # ✅ FIXED: Consistent indentation
  x = 10
  y = 20
  ```

---

### 3. `NameError: name '...' is not defined`
* **What it means in human terms:** You asked Python to use a variable or function name that it has never heard of before.
* **Most common causes:** A typo in the variable name, calling a function before defining it, or forgetting quotation marks around text.
* **Side-by-Side Fix:**
  ```python
  # ❌ BROKEN: 'total' has a typo, and text lacks quotes
  message = Hello
  print(totall)

  # ✅ FIXED: Added quotes and fixed spelling
  message = "Hello"
  print(total)
  ```

---

### 4. `TypeError: can only concatenate str (not "int") to str`
* **What it means in human terms:** You tried to perform an action on incompatible data types (e.g. adding text to a number). Python is **strongly typed** and will never guess what you meant.
* **Most common causes:** Trying to add user input (`input()` always returns text!) to an integer.
* **Side-by-Side Fix:**
  ```python
  # ❌ BROKEN: age is a string '25', cannot add integer 5
  age = "25"
  next_age = age + 5

  # ✅ FIXED: Explicitly convert to int or use f-strings
  age = int("25")
  next_age = age + 5
  print(f"Age in 5 years: {age + 5}")
  ```

---

### 5. `AttributeError: 'NoneType' object has no attribute '...'`
* **What it means in human terms:** You called a method or accessed a property on something that is completely empty (`None`).
* **Most common causes:** Calling a method on a function that didn't `return` a value, or using `.sort()` on a list (which sorts in-place and returns `None`!) instead of `sorted()`.
* **Side-by-Side Fix:**
  ```python
  # ❌ BROKEN: list.sort() returns None!
  numbers = [3, 1, 2]
  sorted_numbers = numbers.sort()
  print(sorted_numbers.append(4))  # Crash! sorted_numbers is None

  # ✅ FIXED:
  numbers = [3, 1, 2]
  numbers.sort()  # Mutates numbers directly
  numbers.append(4)
  # OR use sorted():
  sorted_numbers = sorted(numbers)
  ```

---

### 6. `IndexError: list index out of range`
* **What it means in human terms:** You asked for an element by index that does not exist. Remember that Python uses **0-based indexing**! A list of 3 items only has indices `0`, `1`, and `2`.
* **Most common causes:** Asking for `items[len(items)]` instead of `items[-1]`.
* **Side-by-Side Fix:**
  ```python
  # ❌ BROKEN: List has 3 items (indices 0, 1, 2). Index 3 does not exist!
  items = ["apple", "banana", "cherry"]
  print(items[3])

  # ✅ FIXED: Use index 2 or -1 (last item)
  print(items[2])   # "cherry"
  print(items[-1])  # "cherry"
  ```

---

### 7. `KeyError: '...'`
* **What it means in human terms:** You tried to look up a key in a dictionary with square brackets `dict[key]`, but that key doesn't exist in the dictionary.
* **Most common causes:** Missing dictionary key or typos.
* **Side-by-Side Fix:**
  ```python
  user = {"name": "Alice", "role": "admin"}

  # ❌ BROKEN: 'email' is not in user!
  print(user["email"])

  # ✅ FIXED: Use .get() with a default fallback
  print(user.get("email", "no-email@example.com"))
  ```

---

### 8. `ValueError: invalid literal for int() with base 10: '...'`
* **What it means in human terms:** You told Python to convert a piece of text into a whole number, but the text contains characters that aren't digits (like `"abc"`, `""`, or `"12.5"`).
* **Most common causes:** Converting decimal text `"19.99"` with `int()` instead of `float()`, or blank user input.
* **Side-by-Side Fix:**
  ```python
  # ❌ BROKEN: '19.99' cannot be directly converted to int
  price = int("19.99")

  # ✅ FIXED: Convert to float first
  price = float("19.99")
  int_price = int(float("19.99"))  # 19
  ```

---

### 9. `UnboundLocalError: local variable referenced before assignment`
* **What it means in human terms:** Inside a function, you tried to read or modify a variable before assigning a value to it, or you shadowed an outer variable without using `nonlocal` or `global`.
* **Most common causes:** Doing `count += 1` inside a function where `count` was defined outside.
* **Side-by-Side Fix:**
  ```python
  count = 0

  # ❌ BROKEN: Python treats 'count' as a local variable, but it hasn't been assigned yet!
  def increment():
      count += 1

  # ✅ FIXED: Pass state as an argument and return the result (Idiomatic DRY pattern)
  def increment(current_count: int) -> int:
      return current_count + 1

  count = increment(count)
  ```

---

### 10. `ModuleNotFoundError: No module named '...'`
* **What it means in human terms:** Python cannot find the package or file you are trying to `import`.
* **Most common causes:** You didn't install the package in your current virtual environment, or your terminal is running global Python instead of `.venv\Scripts\python`.
* **Side-by-Side Fix:**
  ```powershell
  # ❌ The package isn't installed in the active environment:
  # Python says: ModuleNotFoundError: No module named 'pydantic'

  # ✅ FIXED: Install using uv or pip inside your virtual environment:
  uv add pydantic
  # Or:
  python -m pip install pydantic
  ```

---

## 🛠️ Modern Debugging Tools: Beyond Basic `print()`

### 1. Self-Documenting Print Statements (`f"{x=}"`)
Did you know Python 3.8+ has a built-in shortcut that prints both the variable name and its value?
```python
name = "Alice"
score = 98.5

# Old tedious way:
print(f"name: {name}, score: {score}")

# Modern effortless way:
print(f"{name=}, {score=}")
# Output: name='Alice', score=98.5
```

---

### 2. Python's Built-in Breakpoint (`breakpoint()`)
Instead of inserting 20 `print()` statements, insert `breakpoint()` directly into your code:

```python
def calculate_order(items):
    total = 0
    for item in items:
        breakpoint()  # 🛑 Python pauses execution right here!
        total += item.price
    return total
```

When Python hits `breakpoint()`, it drops you into an interactive debugger prompt (`(Pdb)`). You can inspect variables and control execution:
- Type any variable name (e.g. `item`) to see its value.
- Type `n` (*next*) to execute the next line.
- Type `s` (*step*) to step inside a function call.
- Type `c` (*continue*) to resume normal execution.
- Type `q` (*quit*) to exit immediately.
