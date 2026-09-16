# Module 02: Self-Assessment Quiz & Mastery Challenges

Test your understanding of functions, parameter rules, scopes (LEGB), closures, and standard libraries before moving to **Module 03**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Return Semantics:** If a Python function executes without encountering an explicit `return` statement, what value is returned to the caller, and what is its data type?
2. **Parameter Syntax:** In `def configure(a, b, /, c, *, d=10, e=20):`, which parameters MUST be passed positionally, and which MUST be passed with keywords?
3. **Variable-Length Arguments:** What Python data structure does `*args` arrive as inside a function? What data structure does `**kwargs` arrive as?
4. **Scope Resolution (LEGB):** When Python resolves a variable name, what are the four scope layers in the exact search order?
5. **Scope Modifiers:** What is the difference in purpose between the `global` and `nonlocal` keywords?
6. **Closure Mechanics:** What is a closure in Python, and how does it retain access to outer variables even after the outer function has finished executing?
7. **The Late Binding Trap:** Why does `[lambda: i for i in range(3)]` cause all three lambdas to return `2` when called, and how do you fix it?
8. **Module Entrypoint:** What is the value of `__name__` when a script is run directly from the terminal versus when it is imported by another module?
9. **Timezone Best Practice:** Why is `datetime.now(timezone.utc)` recommended for backend servers over naive `datetime.now()`?
10. **Argument Unpacking:** How do you pass the dictionary `params = {"host": "localhost", "port": 8080}` into a function `start_server(host, port)` using argument unpacking?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
Python automatically returns the singleton value **`None`**, which belongs to the data type **`NoneType`**.

#### Answer 2:
- `a` and `b` are **positional-only** (because they are before `/`).
- `c` can be passed either positionally or by keyword.
- `d` and `e` are **keyword-only** (because they are after `*`).

#### Answer 3:
- `*args` arrives as a **tuple** (immutable sequence of positional arguments).
- `**kwargs` arrives as a **dict** (dictionary of keyword argument name-value pairs).

#### Answer 4:
1. **L**ocal (inside current function)
2. **E**nclosing (in outer enclosing nested functions)
3. **G**lobal (module-level top-level namespace)
4. **B**uilt-in (Python's built-in namespace like `len`, `range`, `print`)

#### Answer 5:
- `global` tells Python to bind and reassign a variable in the **module-level global namespace**.
- `nonlocal` tells Python to bind and reassign a variable in the **nearest outer enclosing function namespace** (excluding global).

#### Answer 6:
A closure is an inner function that remembers the bindings of free variables in its enclosing scope. When the outer function returns, Python packages those referenced variables into heap-allocated **`cell` objects** stored in the inner function's `__closure__` attribute, preventing them from being garbage-collected.

#### Answer 7:
Closures look up free variables at the time the function is **called** (late binding), not at definition time. When called, the loop has already completed with `i = 2`. Fix it using default parameter evaluation: `[lambda x=i: x for i in range(3)]`.

#### Answer 8:
- When executed directly: `__name__ == "__main__"`.
- When imported: `__name__` is set to the module's file/package name (e.g. `"game_engine.combat"`).

#### Answer 9:
A naive `datetime.now()` contains no timezone offset information and assumes the local server machine clock. If servers are in different regions or observe Daylight Saving Time, timestamps become ambiguous and corrupt chronological ordering. `timezone.utc` ensures a standardized, unambiguous reference point.

#### Answer 10:
Use the dictionary unpacking operator `**`:
```python
start_server(**params)
```

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: The Stateful Rate Limiter Closure

**Goal:** Write a closure factory `create_rate_limiter(max_requests: int)` that returns a validator function.
The validator function should return `True` for the first `max_requests` invocations, and `False` once the quota has been exhausted.

**Requirements:**
1. Do not use global variables or classes.
2. Use `nonlocal` to track remaining requests.
3. Allow resetting the quota if `reset=True` is passed.

<details>
<summary><b>Solution Code</b></summary>

```python
def create_rate_limiter(max_requests: int):
    remaining = max_requests

    def check_request(reset: bool = False) -> bool:
        nonlocal remaining
        if reset:
            remaining = max_requests
            return True

        if remaining > 0:
            remaining -= 1
            return True
        return False

    return check_request

# Verification:
limiter = create_rate_limiter(2)
print(limiter())  # True (1 left)
print(limiter())  # True (0 left)
print(limiter())  # False (Quota exceeded!)
print(limiter(reset=True)) # True (Reset to 2)
print(limiter())  # True (1 left)
```
</details>

---

### Challenge 2: Flexible Dice Roller with `*args`

**Goal:** Create a dice roller `roll_dice(*dice_notations: str) -> dict[str, list[int] | int]` that accepts any number of standard tabletop RPG dice notations (e.g., `"2d6"`, `"1d20"`, `"3d8"`).

**Requirements:**
1. Parse each string formatted as `"<count>d<sides>"`.
2. Generate random rolls using `random.randint(1, sides)`.
3. Return a dictionary containing individual roll lists and the total sum.

<details>
<summary><b>Solution Code</b></summary>

```python
import random

def roll_dice(*dice_notations: str) -> dict[str, object]:
    results = {}
    grand_total = 0

    for notation in dice_notations:
        notation = notation.strip().lower()
        parts = notation.split("d")
        if len(parts) != 2:
            raise ValueError(f"Invalid dice notation format: '{notation}'. Expected 'XdY' (e.g. '2d6').")

        count = int(parts[0])
        sides = int(parts[1])
        
        rolls = [random.randint(1, sides) for _ in range(count)]
        notation_total = sum(rolls)
        grand_total += notation_total

        results[notation] = {
            "rolls": rolls,
            "subtotal": notation_total,
        }

    results["grand_total"] = grand_total
    return results

# Verification:
outcome = roll_dice("2d6", "1d20")
print("Dice Roll Outcome:", outcome)
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Late-binding closure

```python
callbacks = []
for i in range(3):
    callbacks.append(lambda: i)

print([cb() for cb in callbacks])
```

**Observed symptom:** Prints `[2, 2, 2]`. You expected `[0, 1, 2]`.

**(a)** What does each lambda actually capture?

**(b)** Give two fixes.

**(c)** Why is this behaviour correct rather than a bug in Python?

<details>
<summary><b>Show the diagnosis</b></summary>

Each lambda captures the **variable** `i`, not its value at creation time. By the time any of them runs, the loop has finished and `i` is 2.

**Two fixes:** bind at definition with a default argument — `lambda i=i: i` (defaults *are* evaluated eagerly, which is the same mechanism as the mutable-default bug, used deliberately) — or use `functools.partial(lambda x: x, i)`.

**It is correct because** closures capture bindings, which is what makes them useful: a counter closure must see the *current* value of its enclosed variable, not a snapshot from when it was defined. Module 02's rate limiter depends on exactly that. What bites here is creating closures in a loop, where you almost always want a snapshot — so the fix is to ask for one explicitly.

</details>

---

### D2. Missing `nonlocal`

```python
def make_counter():
    count = 0
    def increment():
        count += 1
        return count
    return increment

counter = make_counter()
print(counter())
```

**Observed symptom:** `UnboundLocalError: cannot access local variable 'count' where it is not associated with a value`.

**(a)** Why does assigning to `count` make it local?

**(b)** What keyword fixes it, and what is the alternative?

**(c)** Why does a read-only closure work without any keyword?

<details>
<summary><b>Show the diagnosis</b></summary>

Any **assignment** to a name inside a function makes that name local to the function for its entire body — the compiler decides this statically, before the code runs. `count += 1` is an assignment, so `count` is local, and reading it before assignment raises.

**Fix:** `nonlocal count`, which binds the name to the enclosing function scope. The alternative is to avoid rebinding entirely by mutating a container: `count = [0]` then `count[0] += 1` — mutation is not assignment.

**Read-only closures work** because with no assignment the compiler classifies the name as free, and the LEGB lookup finds it in the enclosing scope naturally. That asymmetry — read is automatic, write needs a declaration — is the single most confusing thing about Python scoping, and `nonlocal` exists precisely to make the write case explicit.

</details>

---

### D3. Shadowed builtin

```python
def summarize(values: list[float]) -> dict[str, float]:
    sum = 0.0
    for v in values:
        sum += v
    max = values[0]
    for v in values:
        if v > max:
            max = v
    return {"total": sum, "peak": max, "count": len(values), "mean": sum / len(values)}

def process(data: list[list[float]]) -> list[float]:
    return [sum(batch) for batch in data]
```

**Observed symptom:** `summarize` works. `process`, called later in the same module, raises `TypeError: 'float' object is not callable`.

**(a)** Why does `process` fail when the shadowing happened in a different function?

**(b)** What actually broke?

**(c)** What tool catches this before runtime?

<details>
<summary><b>Show the diagnosis</b></summary>

It does not — read the traceback carefully. `sum` inside `summarize` is **local** to `summarize` and cannot affect `process`. The real failure is that somewhere a **module-level** `sum = ...` was introduced (or `from x import sum`), which shadows the builtin for the whole module.

The lesson is the diagnostic one: local shadowing is harmless and ugly; *module-level* shadowing is action at a distance, breaking code that never mentioned the name.

**What broke:** the builtin `sum` is resolved at call time via LEGB, and a module-global binding is found before builtins.

**Caught by** `ruff`'s flake8-builtins rules (`A001`/`A002`), which flag any assignment shadowing a builtin. Even for the harmless local case, renaming to `total` and `peak` costs nothing and removes the whole question.

</details>

---

### D4. Argument unpacking order

```python
def connect(host: str, port: int = 5432, *, timeout: float = 5.0) -> str:
    return f"{host}:{port} t={timeout}"

config = {"host": "db.internal", "timeout": 10.0}
print(connect(*config))
```

**Observed symptom:** Prints `host:timeout t=5.0` — the keys were passed as positional values.

**(a)** What did `*config` unpack?

**(b)** What is the correct operator?

**(c)** Why can `timeout` never be passed positionally here?

<details>
<summary><b>Show the diagnosis</b></summary>

Iterating a dict yields its **keys**, so `*config` passed the strings `"host"` and `"timeout"` as `host` and `port`.

**Correct:** `connect(**config)` — the double star unpacks a mapping into keyword arguments.

**`timeout` is keyword-only** because of the bare `*` in the signature: every parameter after it can only be supplied by name. That is a deliberate API design choice — it prevents `connect("db", 5432, 10.0)`, where the reader cannot tell what `10.0` means, and it lets you reorder or insert keyword-only parameters later without breaking callers. Use it for any parameter whose meaning is not obvious from position.

</details>

---

### D5. Decorator applied at the wrong time

```python
import functools

def cache_result(fn):
    @functools.wraps(fn)
    def wrapper(*args):
        if not hasattr(wrapper, "_value"):
            wrapper._value = fn(*args)
        return wrapper._value
    return wrapper

@cache_result
def get_config(env: str) -> dict:
    return {"env": env}

print(get_config("dev"))
print(get_config("prod"))
```

**Observed symptom:** Prints `{'env': 'dev'}` twice.

**(a)** Why does the second call return the first result?

**(b)** What is the minimal fix?

**(c)** What should you use instead of hand-rolling this?

<details>
<summary><b>Show the diagnosis</b></summary>

The cache is stored on the **wrapper function object**, which is a single object shared by all calls. It ignores the arguments entirely — the first result is returned for every input forever.

**Minimal fix:** key the cache by the arguments:
```python
wrapper._cache = {}
if args not in wrapper._cache:
    wrapper._cache[args] = fn(*args)
return wrapper._cache[args]
```

**Use instead:** `functools.lru_cache` (or `functools.cache`), which handles argument keying, keyword arguments, a size bound, thread safety and hit/miss statistics — all things this hand-rolled version gets wrong. Module 20 covers when `lru_cache` is *not* enough (TTLs, sharing across processes) and what to reach for then.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites a real file or test in this course. Open them —
the fix is not hypothetical, it is in the code you already have.
