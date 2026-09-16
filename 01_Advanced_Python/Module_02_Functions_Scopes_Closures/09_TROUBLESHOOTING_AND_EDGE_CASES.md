# Module 02: Troubleshooting, Scope Bugs & Edge Cases

This guide details the most notorious bugs and edge cases related to functions, variable scopes, closures, and modular imports in Python.

---

## 1. `UnboundLocalError: local variable referenced before assignment`

### The Bug
```python
score = 100

def increase_score():
    print(f"Current score is: {score}")  # ❌ Crash!
    score = score + 10

increase_score()
```
**Crash:** `UnboundLocalError: local variable 'score' referenced before assignment`

### Why It Happens
Python analyzes function bodies **at compile-time**. When Python sees `score = ...` anywhere inside `increase_score()`, it marks `score` as a **Local variable for the entire function**.
When `print(score)` runs on line 4, Python looks for the *local* `score`, which hasn't been assigned a value yet!

### The Fix
If you intended to modify the global variable, declare `global`:
```python
score = 100

def increase_score():
    global score
    print(f"Current score is: {score}")
    score += 10
```
*(Best Practice: Avoid global variables entirely by passing `score` as an argument and returning the new value).*

---

## 2. The Closure Loop Trap (Late Binding)

### The Bug
```python
# Create a list of 3 multiplier functions:
multipliers = []
for i in range(3):
    multipliers.append(lambda x: x * i)

# Call each function with 10:
for f in multipliers:
    print(f(10))
```
**Expected Output:** `0, 10, 20`
**Actual Output:** `20, 20, 20` (Surprise!)

### Why It Happens
Python closures use **late binding**: the inner lambda looks up the variable `i` when the function is **called**, not when it was defined. By the time the loop ends and you call `f(10)`, `i` has reached its final value `2`.

### The Fix: Default Argument Binding
Default arguments are evaluated **at definition time**. Use a default parameter to capture the current value of `i`:
```python
multipliers = []
for i in range(3):
    multipliers.append(lambda x, step=i: x * step)  # 'step' is captured immediately!

for f in multipliers:
    print(f(10))  # Output: 0, 10, 20
```

---

## 3. `nonlocal` Reassignment vs. In-Place Mutation

### The Observation
```python
def make_list_manager():
    items = []       # List object
    counter = 0      # Integer number

    def add_item(val):
        items.append(val)  # ✅ Works WITHOUT nonlocal!
        # counter += 1     # ❌ UnboundLocalError without nonlocal!

    return add_item
```

### Why It Happens
* `items.append(val)` modifies an existing object **in-place** (it does not reassign the variable name `items`).
* `counter += 1` is syntactic sugar for `counter = counter + 1`, which is an **assignment**! Without `nonlocal counter`, Python treats `counter` as a brand-new local variable.

### Rule
- **Calling methods on objects (`.append()`, `.update()`, `.pop()`):** No `nonlocal` needed.
- **Reassigning variable names (`x = ...`, `x += ...`):** `nonlocal` is required.

---

## 4. Circular Import Errors

### The Bug
* `module_a.py` imports `module_b`
* `module_b.py` imports `module_a`

**Crash:** `ImportError: cannot import name 'X' from partially initialized module`

### Why It Happens
When `module_a` runs, it pauses to load `module_b`. But `module_b` immediately pauses to load `module_a`, creating a circular deadlock before either module can finish initializing its functions.

### The Fix
1. **Refactor Shared Logic:** Move shared models, constants, or types into a third file `common.py` or `types.py`.
2. **Import Inside Function (Lazy Import):** If unavoidable, move the `import` statement inside the specific function that uses it.

---

## 5. Shadowing Built-in Python Names

### The Bug
```python
# Bad practice:
def calculate_grades(list, sum):
    total = sum(list)  # ❌ TypeError: 'int' object is not callable
```

### Why It Happens
By naming your parameters `list` and `sum`, you hid Python's built-in `list` type and `sum()` function within that scope!

### Clean Naming Alternatives:
* Instead of `list` $\rightarrow$ use `items`, `values`, `elements`
* Instead of `dict` $\rightarrow$ use `data`, `lookup`, `mapping`
* Instead of `sum` $\rightarrow$ use `total`, `aggregate`
* Instead of `id` $\rightarrow$ use `user_id`, `item_id`, `identifier`
* Instead of `type` $\rightarrow$ use `category`, `kind`, `item_type`
