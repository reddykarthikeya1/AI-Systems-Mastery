# Module 01: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Python fundamentals, primitive data types, memory semantics, and control flow before moving to **Module 02**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Execution Model:** In Python, what is the role of Bytecode (`.pyc`), and why doesn't Python compile directly to raw machine code like C++ or Go?
2. **Type System:** Why is Python considered both *Dynamically Typed* and *Strongly Typed*? Give a short example illustrating each.
3. **Memory & Identity:** If `list_a = [10, 20]` and `list_b = [10, 20]`, what are the outputs of `list_a == list_b` and `list_a is list_b`? Why do they differ?
4. **Division Mechanics:** What is the difference in behavior and return type between `15 / 4` and `15 // 4`?
5. **Floating-Point Quirks:** Why does `0.1 + 0.2 == 0.3` evaluate to `False` in standard Python, and what standard library module should you use for exact monetary calculations?
6. **Logical Short-Circuiting:** In the expression `x != 0 and (100 / x) > 5`, why does Python NOT crash with a `ZeroDivisionError` when `x = 0`?
7. **String Slicing:** Given the string `s = "PYTHONIC"`, what does `s[1:6:2]` return? Explain how `start`, `stop`, and `step` work here.
8. **f-String Formatting:** How do you format a float `num = 1234567.891` so that it displays with commas as thousands separators and rounded to 2 decimal places?
9. **Loop Else Clause:** When does the `else` block attached to a `for` or `while` loop execute? When is it skipped?
10. **Pattern Matching:** How does `match-case` in Python 3.10+ handle wildcard matching (equivalent to a default `else` branch)?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
Bytecode is a platform-independent, simplified intermediate instruction set. Compiling to bytecode allows Python to be write-once, run-anywhere (cross-platform): the CPython Virtual Machine executes bytecode on Windows, macOS, and Linux without recompiling source code for each specific CPU architecture.

#### Answer 2:
- **Dynamically typed:** Variable names are not bound to a fixed type; a variable can point to an `int` and later point to a `str` (`x = 5; x = "hello"`).
- **Strongly typed:** Python strictly enforces types and will not perform silent implicit conversions between incompatible types (e.g., `"5" + 5` raises a `TypeError` rather than producing `"55"` or `10`).

#### Answer 3:
- `list_a == list_b` is **`True`** because `==` checks value equality (both lists contain `10, 20`).
- `list_a is list_b` is **`False`** because `is` checks memory address identity. Each list bracket `[...]` creates a new, separate list object in RAM.

#### Answer 4:
- `15 / 4` is **True Division**: it returns a float `3.75`.
- `15 // 4` is **Floor Division**: it rounds down towards negative infinity and returns an integer `3`.

#### Answer 5:
Computers use binary (base-2) IEEE 754 floating-point numbers. Decimal fractions like $0.1$ ($1/10$) repeat infinitely in binary and cannot be stored exactly, yielding $0.30000000000000004$. For exact financial calculations, use the **`decimal.Decimal`** module.

#### Answer 6:
Python uses **short-circuit evaluation**. In an `and` expression, if the left operand (`x != 0`) is `False`, the entire condition is guaranteed to be `False`, so Python immediately stops and never evaluates `(100 / x) > 5`, preventing the division by zero.

#### Answer 7:
`s[1:6:2]` returns **`"YHN"`**.
- Start at index `1` (`'Y'`).
- Stop before index `6` (stops before `'I'`).
- Step by `2`: picks index 1 (`'Y'`), index 3 (`'H'`), and index 5 (`'N'`).

#### Answer 8:
Use the formatting specifier `{num:,.2f}`:
```python
num = 1234567.891
print(f"${num:,.2f}")  # Output: $1,234,567.89
```

#### Answer 9:
The loop `else` block executes **only if the loop completed naturally** (i.e., finished all iterations of a `for` loop or the `while` condition became `False`). It is **skipped if the loop exited via a `break` statement**.

#### Answer 10:
Use the single underscore wildcard `case _:` at the end of the `match` block. It acts as a catch-all for any pattern not matched by previous `case` statements.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: The Temperature Converter with Pattern Matching

**Goal:** Write a function `convert_temperature(value: float, from_unit: str, to_unit: str) -> float` that supports converting between Celsius (`"C"`), Fahrenheit (`"F"`), and Kelvin (`"K"`).

**Formulas:**
* $F = (C \times 9/5) + 32$
* $C = (F - 32) \times 5/9$
* $K = C + 273.15$

**Requirements:**
1. Use `match (from_unit.upper(), to_unit.upper()):` to handle conversions cleanly.
2. Return rounded results to 2 decimal places.
3. If units are identical, return the original value.

<details>
<summary><b>Solution Code</b></summary>

```python
def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    unit_pair = (from_unit.strip().upper(), to_unit.strip().upper())
    
    match unit_pair:
        case (u1, u2) if u1 == u2:
            return round(value, 2)
        case ("C", "F"):
            return round((value * 9 / 5) + 32, 2)
        case ("F", "C"):
            return round((value - 32) * 5 / 9, 2)
        case ("C", "K"):
            return round(value + 273.15, 2)
        case ("K", "C"):
            return round(value - 273.15, 2)
        case ("F", "K"):
            celsius = (value - 32) * 5 / 9
            return round(celsius + 273.15, 2)
        case ("K", "F"):
            celsius = value - 273.15
            return round((celsius * 9 / 5) + 32, 2)
        case _:
            raise ValueError(f"Unsupported unit conversion from {from_unit} to {to_unit}")

# Verification:
print(convert_temperature(100, "C", "F"))   # 212.0
print(convert_temperature(32, "F", "C"))    # 0.0
print(convert_temperature(0, "C", "K"))     # 273.15
```
</details>

---

### Challenge 2: Robust Number Guessing Game Loop

**Goal:** Create a terminal mini-game where the computer picks a secret number between 1 and 20, and the player has 5 attempts to guess it.

**Requirements:**
1. Handle invalid inputs (e.g. letters or numbers outside 1–20) gracefully without crashing.
2. Provide feedback: `"Too high!"`, `"Too low!"`, or `"Correct!"`.
3. Use a `for-else` loop structure: if the player runs out of attempts, use the `else` clause to reveal the secret number.

<details>
<summary><b>Solution Code</b></summary>

```python
import random

def play_guessing_game() -> None:
    secret_number = random.randint(1, 20)
    max_attempts = 5
    print("=== Guess the Secret Number (1 to 20) ===")

    for attempt in range(1, max_attempts + 1):
        raw_input = input(f"Attempt {attempt}/{max_attempts} -> Enter your guess: ")
        
        # Robust validation
        try:
            guess = int(raw_input)
            if not (1 <= guess <= 20):
                print("Please enter a number within the range 1 to 20.")
                continue
        except ValueError:
            print("Invalid input! Please enter a whole number.")
            continue

        if guess == secret_number:
            print(f"🎉 Congratulations! You guessed the secret number {secret_number} in {attempt} attempts!")
            break
        elif guess < secret_number:
            print("📈 Too low! Try a higher number.")
        else:
            print("📉 Too high! Try a lower number.")
    else:
        # Runs only if the player never hit 'break'
        print(f"😢 Game Over! You've used all attempts. The secret number was {secret_number}.")

if __name__ == "__main__":
    play_guessing_game()
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Float equality in a loop condition

```python
total = 0.0
while total != 1.0:
    total += 0.1
    print(total)
```

**Observed symptom:** Infinite loop. The printed values pass 1.0 and keep going.

**(a)** Why is `total` never exactly 1.0?

**(b)** Give two correct rewrites.

**(c)** What does `0.1 + 0.2 == 0.3` evaluate to, and why does that matter here?

<details>
<summary><b>Show the diagnosis</b></summary>

0.1 has no exact binary representation, so accumulating it ten times gives `0.9999999999999999`, then `1.0999999999999999`. The loop condition is never satisfied.

**Two rewrites:** count integers and scale — `for i in range(10): total = i / 10` — or compare with a tolerance: `while abs(total - 1.0) > 1e-9`. The first is better: it removes the accumulation error entirely rather than tolerating it.

**`0.1 + 0.2 == 0.3` is `False`** (the sum is `0.30000000000000004`). It matters because it is the same defect in miniature: never use `==` or `!=` on accumulated floats. For money, use `Decimal` — Module 08's ledger does, precisely to avoid this.

</details>

---

### D2. Mutable default argument

```python
def add_item(item: str, basket: list[str] = []) -> list[str]:
    basket.append(item)
    return basket

print(add_item("apple"))
print(add_item("bread"))
```

**Observed symptom:** Prints `['apple']`, then `['apple', 'bread']` — the second call inherited the first call's basket.

**(a)** When exactly is the default list created?

**(b)** What is the correct pattern?

**(c)** Which immutable defaults are safe, and why does that make this bug worse?

<details>
<summary><b>Show the diagnosis</b></summary>

**Once**, when the `def` statement executes — not per call. Every call that omits the argument shares that one list object, so mutations accumulate across calls.

**Correct:**
```python
def add_item(item: str, basket: list[str] | None = None) -> list[str]:
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```

**Immutable defaults are safe** — `0`, `""`, `None`, `(1, 2)` — because you cannot mutate them; rebinding creates a new object. That is what makes this bug worse: 95% of default arguments are immutable and behave intuitively, so the mutable case violates an expectation you have built up over hundreds of correct functions. `ruff` flags it as `B006`, and this course enables that rule.

</details>

---

### D3. `is` versus `==`

```python
def is_target(n: int) -> bool:
    return n is 1000

print(is_target(1000))
print(is_target(int("1000")))
```

**Observed symptom:** Prints `True`, then `False`.

**(a)** Explain the difference between the two calls.

**(b)** When is `is` the correct operator?

**(c)** Why is the first call `True` at all?

<details>
<summary><b>Show the diagnosis</b></summary>

`is` compares **identity** — whether two names point at the same object. `==` compares **value**. `int("1000")` constructs a new object, so it is a different object with an equal value.

**`is` is correct only for singletons**: `None`, `True`, `False`, and sentinels you created yourself (`MISSING = object()`, as in Module 20's cache). Never for numbers, strings, or containers.

**The first call is `True`** because CPython's compiler folds identical literal constants within one code object, so both `1000`s are the same object. That is an implementation detail that has changed between versions and differs in the REPL — which is exactly why you must not rely on it. Modern Python emits a `SyntaxWarning` for `is` against a literal, and `ruff` flags it as `F632`.

</details>

---

### D4. Off-by-one in a range

```python
def sum_to(n: int) -> int:
    """Sum every integer from 1 to n inclusive."""
    return sum(range(1, n))

print(sum_to(10))
```

**Observed symptom:** Prints `45`. The correct answer is 55.

**(a)** What is `range(1, 10)` actually?

**(b)** What is the fix?

**(c)** What is the design reason Python's ranges exclude the stop value?

<details>
<summary><b>Show the diagnosis</b></summary>

`range(1, 10)` yields 1 through **9** — the stop value is exclusive. So the sum omits 10.

**Fix:** `range(1, n + 1)`.

**Why exclusive:** it makes `len(range(a, b))` equal `b - a`, makes adjacent ranges join cleanly (`range(0,3)` + `range(3,6)` covers 0–5 with no overlap and no gap), and matches zero-based indexing so `range(len(xs))` covers exactly the valid indices. Every one of those properties would break with an inclusive stop. The convention costs you one off-by-one bug early and saves a dozen later — which is why writing a test against a known value (`sum_to(10) == 55`) catches it immediately.

</details>

---

### D5. String immutability in a loop

```python
def build_csv(rows: list[list[str]]) -> str:
    out = ""
    for row in rows:
        for cell in row:
            out += cell + ","
        out = out[:-1] + "\n"
    return out
```

**Observed symptom:** Correct output, but processing 100,000 rows takes minutes.

**(a)** Why is this quadratic rather than linear?

**(b)** What is the linear rewrite?

**(c)** Which line is the worse offender, and why?

<details>
<summary><b>Show the diagnosis</b></summary>

Strings are **immutable**, so `out += cell` allocates a whole new string and copies everything accumulated so far. Over n appends the total work is O(n²).

**Linear rewrite:**
```python
return "\n".join(",".join(row) for row in rows) + "\n"
```
One pass, one allocation per join.

**`out = out[:-1] + "\n"` is worse** than the `+=`: slicing copies the entire accumulated string, *then* the concatenation copies it again — two full copies per row rather than one. It also hides a correctness bug: on an empty row it strips a character it did not add. Module 12's diagnostic on `dis.dis` shows the bytecode behind this, including why CPython's in-place `+=` optimisation makes the problem invisible in microbenchmarks.

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
