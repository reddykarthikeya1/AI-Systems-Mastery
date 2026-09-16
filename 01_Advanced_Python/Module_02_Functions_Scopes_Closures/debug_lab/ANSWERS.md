# Debug Lab Answers: Module 02

<details>
<summary>Bug 1: Shadowed built-in function</summary>

### Root Cause
At line 4, `sum = 100` binds the name `sum` in global module scope to an integer, overwriting the built-in function `builtins.sum`. When `calculate_team_score` calls `sum(...)`, Python tries to call `100(...)`.

### Fix
Rename the variable to avoid collision with standard library built-ins:
```python
INITIAL_RESERVE_POINTS = 100
```
</details>

<details>
<summary>Bug 2: Mutable default argument</summary>

### Root Cause
Default argument values are evaluated once when the function is defined, not every time it is called. Every invocation that omits `tags` mutates that exact same shared list in memory.

### Fix
Use `None` as a sentinel value and instantiate a new list inside the function:
```python
def create_inventory_item(item_name: str, tags: list[str] | None = None) -> list[str]:
    if tags is None:
        tags = []
    tags.append(item_name)
    return tags
```
</details>

<details>
<summary>Bug 3: Late-binding closures in a loop</summary>

### Root Cause
Closures in Python look up the variable `i` in the enclosing scope when called, not when created. At the end of the loop, `i == 2`, so every lambda evaluates `x * 2`.

### Fix
Bind `i` at definition time using a default parameter:
```python
def make_multiplier_handlers():
    return [lambda x, factor=i: x * factor for i in range(3)]
```
</details>
