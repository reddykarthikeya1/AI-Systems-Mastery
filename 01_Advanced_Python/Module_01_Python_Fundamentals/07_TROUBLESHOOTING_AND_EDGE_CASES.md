# Module 01: Troubleshooting, Common Bugs & Beginner Traps

Here are the most frequent pitfalls and errors beginners encounter in Python syntax, data types, control flow, and pattern matching, along with deep explanations and fixes.

---

## 1. `TypeError: can only concatenate str (not "int") to str`

### The Bug
```python
age = input("Enter your age: ")
print("In 5 years you will be: " + age + 5)
```
**Crash:** `TypeError: can only concatenate str (not "int") to str`

### Why It Happens
1. `input()` **always** returns a string (`str`), even if the user typed digits.
2. Python is **strongly typed**—it will never automatically convert `"25"` to `25`.
3. In Python, `+` on strings means text concatenation, while `+` on numbers means arithmetic addition.

### The Fix
Convert user input using `int()` or `float()`, and use modern f-strings:
```python
age = int(input("Enter your age: "))
print(f"In 5 years you will be: {age + 5}")
```

---

## 2. The `match-case` Syntax Error: Direct Comparison Expressions Inside `case`

### The Bug
```python
number = 100

match number:
    case number > 10:   # ❌ SyntaxError: invalid syntax!
        print(True)
    case number < 90:
        print(True)
```
**Crash:** `SyntaxError: invalid syntax`

### Why It Happens
In Python's `match-case` (Structural Pattern Matching):
1. `case` expects a **Pattern** (such as a literal value `case 10:`, a structure `case [x, y]:`, or a variable name to capture into `case n:`).
2. It does **not** accept comparison expressions like `> 10` or `< 90` directly in the pattern position.

### The Fix: Use Pattern Guards with `if`
To test ranges or boolean conditions in `match-case`, assign a variable name (a **capture pattern**) and append an **`if` guard**:
```python
number = 100

match number:
    case n if n > 10:   # ✅ 'n' captures the number (n = 100), 'if n > 10' checks condition!
        print("Greater than 10:", n)
    case n if n < 90:
        print("Less than 90:", n)
    case _:
        print("Default match")
```

---

## 3. The `range()` Off-by-One Trap

### The Bug
```python
# Goal: Print numbers 1 through 5
for i in range(1, 5):
    print(i)
```
**Output:**
```
1
2
3
4
```
*(Notice number 5 was never printed!)*

### Why It Happens
In Python, ranges and slices always operate as **half-open intervals**: `[start, stop)`. The `stop` value is **exclusive** (meaning "stop *before* reaching this number").

### The Fix
To include 5, write `range(1, 6)` or `range(1, target + 1)`:
```python
for i in range(1, 6):
    print(i)
```

---

## 4. The `is` vs `==` Small Integer Trap

### The Bug
```python
x = 256
y = 256
print(x is y)  # True!

a = 1000
b = 1000
print(a is b)  # False! (Surprise!)
```

### Why It Happens
CPython pre-allocates and caches small integers between **-5 and 256** in memory for performance. So `256` always points to the same cached memory object, but `1000` creates separate memory allocations.

### The Rule
* **NEVER** use `is` to compare numbers or values!
* **ALWAYS** use `==` for values: `a == b` will correctly be `True`.
* Only use `is` for singletons like `None`: `if result is None:`.

---

## 5. Float Equality Comparison Trap

### The Bug
```python
total = 0.1 + 0.2
if total == 0.3:
    print("Exact match!")
else:
    print("Mismatch!")  # This prints!
```

### Why It Happens
Computers store floating-point numbers in binary (base-2). Decimal fractions like `0.1` cannot be stored with infinite precision in binary, resulting in `0.30000000000000004`.

### The Fix
Use `math.isclose()` for scientific/engineering code, or `decimal.Decimal` for financial code:
```python
import math
if math.isclose(total, 0.3):
    print("Close enough match!")
```

---

## 6. Infinite `while` Loops

### The Bug
```python
count = 5
while count > 0:
    print(f"Countdown: {count}")
    # Forgot to decrement count!
```
The program freezes your terminal by printing `Countdown: 5` forever.

### The Fix
Always ensure the condition variable changes inside the loop body, or provide a safety `break`:
```python
count = 5
while count > 0:
    print(f"Countdown: {count}")
    count -= 1  # Crucial update!
```
*(Tip: In your terminal, press `Ctrl + C` to terminate an infinite loop).*

---

## 7. String Slicing Out-of-Bounds Behavior

### Observation
```python
s = "Hello"
# print(s[10])   # ❌ IndexError: string index out of range
print(s[2:100])   # ✅ Returns 'llo' without error!
```

### Why It Happens
* Single indexing (`s[i]`) strictly checks bounds and throws `IndexError` if the index does not exist.
* Slicing (`s[start:stop]`) is forgiving—Python automatically clamps the indices to the string length.

---

## 8. "Why Did My Functions Define But Not Print Anything?"

### The Observation
You define functions with `print()` inside them, run the file, and nothing displays on screen.

### Why It Happens
Writing `def my_func():` only loads the instructions into memory. It does not execute until you call `my_func()`.

### The Fix
Add an explicit execution call or entry point:
```python
def calculate():
    print("Result calculated!")

if __name__ == "__main__":
    calculate()  # <-- Triggers execution!
```
