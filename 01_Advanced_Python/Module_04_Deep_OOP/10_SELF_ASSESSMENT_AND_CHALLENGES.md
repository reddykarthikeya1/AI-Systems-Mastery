# Module 04: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Object-Oriented Programming (OOP), properties, inheritance, MRO, and dunder protocols before moving to **Module 05**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Object Lifecycle:** What is the technical difference in responsibility between `__new__` and `__init__` when creating a new class instance?
2. **Method Types:** When should you use a `@classmethod` instead of a standard instance method or `@staticmethod`?
3. **Encapsulation:** In Python, what does the double leading underscore (e.g. `self.__secret_key`) actually do to the variable name?
4. **Property Protocol:** Why are Python properties (`@property`) preferred over Java-style `get_value()` and `set_value()` methods?
5. **Multiple Inheritance (MRO):** How does Python determine which method to call when two parent classes define a method with the exact same name?
6. **String Representations:** What is the rule of thumb difference in purpose between `__str__` and `__repr__`?
7. **The Equality-Hash Contract:** If you override `__eq__` on a custom class, why must you also override `__hash__` if instances will be stored in sets or dictionary keys?
8. **Class State:** If you define `tags = []` at the class level outside `__init__`, what happens when multiple instances call `self.tags.append("item")`?
9. **Abstract Interfaces:** What happens if a subclass fails to implement an `@abstractmethod` defined in its parent `abc.ABC` class?
10. **`super()` Mechanics:** When calling `super().some_method()`, does Python look directly at the parent class or follow the current object's MRO chain?

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
- `__new__(cls)` is the **constructor**: it allocates the raw memory and returns the newly created instance.
- `__init__(self)` is the **initializer**: it accepts the newly allocated instance and configures its attributes.

#### Answer 2:
Use `@classmethod` when you need access to the class object itself (`cls`) rather than a specific instance—most commonly to implement **alternative factory constructors** (e.g., `Date.from_timestamp(ts)` or `User.from_json(raw)`).

#### Answer 3:
It triggers **Name Mangling**: Python automatically prefixes the attribute name with `_ClassName` (e.g. `self.__secret_key` becomes `self._Account__secret_key`) to prevent accidental naming collisions in subclasses.

#### Answer 4:
Properties maintain a clean, pythonic public API (`account.balance = 500`) while allowing you to add validation, computations, and access logging under the hood without breaking backwards compatibility for callers.

#### Answer 5:
Python follows the **Method Resolution Order (MRO)** computed via the **C3 Linearization algorithm**, which guarantees that child classes precede parent classes and multiple parents are checked in left-to-right order.

#### Answer 6:
- `__str__` is intended for **end-users**: human-readable, friendly, and clean.
- `__repr__` is intended for **developers/debuggers**: unambiguous, detailed, and ideally valid Python code that could recreate the object (`eval(repr(obj)) == obj`).

#### Answer 7:
If two objects are equal (`a == b`), they must produce the exact same hash value (`hash(a) == hash(b)`). Overriding `__eq__` without `__hash__` breaks hash table invariants, leading to lost or duplicate entries in sets/dictionaries.

#### Answer 8:
All instances share and mutate the **same single list in RAM**, leading to accidental cross-instance data contamination.

#### Answer 9:
Python raises a `TypeError` at **instantiation time** (`TypeError: Can't instantiate abstract class ...`), preventing the object from ever being created.

#### Answer 10:
`super()` dynamically follows the **Method Resolution Order (MRO)** chain of the `self` instance, which enables clean cooperative multiple inheritance.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Custom Fraction Number Class

**Goal:** Build an immutable `Fraction` class supporting exact rational arithmetic.

**Requirements:**
1. `__init__(self, numerator: int, denominator: int)`: Automatically reduces fraction using `math.gcd` and rejects `denominator == 0`.
2. Implement `__repr__` (`"Fraction(1, 2)"`) and `__str__` (`"1/2"`).
3. Implement `__add__` ($a/b + c/d = (ad + bc) / bd$) and `__eq__`.

<details>
<summary><b>Solution Code</b></summary>

```python
import math

class Fraction:
    def __init__(self, numerator: int, denominator: int) -> None:
        if denominator == 0:
            raise ZeroDivisionError("Fraction denominator cannot be zero.")
        
        # Simplify using Greatest Common Divisor
        common = math.gcd(numerator, denominator)
        # Handle sign normalization (keep denominator positive)
        sign = -1 if denominator < 0 else 1
        self._num = (numerator // common) * sign
        self._den = abs(denominator // common)

    @property
    def numerator(self) -> int: return self._num
    @property
    def denominator(self) -> int: return self._den

    def __repr__(self) -> str:
        return f"Fraction({self._num}, {self._den})"

    def __str__(self) -> str:
        return f"{self._num}/{self._den}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Fraction):
            return self._num == other._num and self._den == other._den
        return False

    def __add__(self, other: Fraction) -> Fraction:
        if not isinstance(other, Fraction):
            raise TypeError("Can only add Fraction to Fraction.")
        new_num = (self._num * other._den) + (other._num * self._den)
        new_den = self._den * other._den
        return Fraction(new_num, new_den)

# Verification:
f1 = Fraction(1, 2)
f2 = Fraction(2, 4)  # Automatically simplifies to 1/2
f3 = Fraction(1, 3)

print(f"f1 == f2 : {f1 == f2}")       # True
print(f"f1 + f3  : {f1 + f3}")        # 5/6
print(f"f1 (repr): {f1!r}")           # Fraction(1, 2)
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Shared mutable class attribute

```python
class Account:
    transactions = []          # class attribute

    def __init__(self, owner: str) -> None:
        self.owner = owner

    def deposit(self, amount: float) -> None:
        self.transactions.append(amount)

a, b = Account("ada"), Account("bob")
a.deposit(100)
print(b.transactions)
```

**Observed symptom:** Prints `[100]` — Bob sees Ada's deposit.

**(a)** Why does Bob's account contain Ada's transaction?

**(b)** What is the one-line fix?

**(c)** What would the same code do if `transactions` were an `int` instead of a `list`?

<details>
<summary><b>Show the diagnosis</b></summary>

`transactions = []` is a **class** attribute, created once when the class body executes, and shared by every instance. `self.transactions.append(...)` looks up the name on the instance, fails, falls back to the class, and mutates the shared list.

**Fix:** move it into `__init__` — `self.transactions: list[float] = []` — or use `field(default_factory=list)` in a dataclass.

**With an `int`:** the bug would *hide*. `self.count += 1` rebinds rather than mutates, creating a genuine instance attribute on first write. That is why this bug is associated with mutable defaults specifically — immutable ones mask it.

</details>

---

### D2. `__eq__` without `__hash__`

```python
class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)

seen = {Point(1, 2)}
print(Point(1, 2) in seen)
```

**Observed symptom:** Raises `TypeError: unhashable type: 'Point'`.

**(a)** Why did defining `__eq__` make the class unhashable?

**(b)** What are the two correct fixes, and when would you choose each?

**(c)** What breaks if you define `__hash__` but leave it inconsistent with `__eq__`?

<details>
<summary><b>Show the diagnosis</b></summary>

Defining `__eq__` sets `__hash__ = None` implicitly. Python enforces the invariant that equal objects must hash equally; since it cannot infer your equality semantics, it removes hashability rather than let you violate it silently.

**Fix 1** — define `__hash__ = lambda self: hash((self.x, self.y))` (do it properly as a method) when the object is logically immutable. **Fix 2** — use `@dataclass(frozen=True)`, which generates both consistently.

**Inconsistent hash:** two equal objects with different hashes land in different buckets, so `in` returns `False` for an object that *is* present, and a dict can hold two keys that compare equal. Corruption that surfaces far from the cause.

</details>

---

### D3. MRO and cooperative `super()`

```python
class Base:
    def __init__(self) -> None:
        self.log = ["Base"]

class Audited(Base):
    def __init__(self) -> None:
        Base.__init__(self)
        self.log.append("Audited")

class Timed(Base):
    def __init__(self) -> None:
        Base.__init__(self)
        self.log.append("Timed")

class Service(Audited, Timed):
    def __init__(self) -> None:
        Audited.__init__(self)
        Timed.__init__(self)

print(Service().log)
```

**Observed symptom:** Prints `['Base', 'Timed']` — the `Audited` entry vanished.

**(a)** Why is `'Audited'` missing from the log?

**(b)** How does replacing the explicit calls with `super().__init__()` fix it?

**(c)** What is `Service.__mro__` here?

<details>
<summary><b>Show the diagnosis</b></summary>

`Timed.__init__` calls `Base.__init__`, which **reassigns** `self.log = ['Base']`, discarding the `'Audited'` entry appended moments earlier. Explicit parent calls run `Base.__init__` twice.

**Fix:** cooperative inheritance — every class calls `super().__init__()` exactly once, and Python walks the MRO linearly so `Base` runs only once: `['Base', 'Timed', 'Audited']`.

**MRO:** `Service -> Audited -> Timed -> Base -> object`. Check it with `Service.__mro__`. This is the entire reason `super()` exists and why calling parents by name in a diamond is a bug.

</details>

---

### D4. `__slots__` silently defeated

```python
class Compact:
    __slots__ = ("x", "y")

class Sub(Compact):
    pass

s = Sub()
s.anything = 42
print(hasattr(s, "__dict__"))
```

**Observed symptom:** Prints `True`, and the memory saving `__slots__` promised is gone.

**(a)** Why does the subclass have a `__dict__`?

**(b)** What must `Sub` declare to keep the saving?

**(c)** How would you measure whether it worked?

<details>
<summary><b>Show the diagnosis</b></summary>

A subclass that does not declare its own `__slots__` gets a `__dict__` automatically, so instances of `Sub` carry both the slots *and* a dict — larger than a plain class.

**Fix:** `class Sub(Compact): __slots__ = ()`. An empty tuple is the declaration that says 'no new attributes'.

**Measure it** with `sys.getsizeof` plus `__sizeof__`, or `tracemalloc` over 100k instances. Module 21 adds a `@pytest.mark.perf` test for exactly this; a claim about memory that is not measured is not a claim.

</details>

---

### D5. Property that shadows its own setter

```python
class Temperature:
    def __init__(self, celsius: float) -> None:
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("below absolute zero")
        self.celsius = value        # <-- note this line

t = Temperature(20)
```

**Observed symptom:** `RecursionError: maximum recursion depth exceeded`.

**(a)** Trace the recursion. What calls what?

**(b)** What is the fix?

**(c)** Why did `__init__` not bypass the property?

<details>
<summary><b>Show the diagnosis</b></summary>

The setter assigns to `self.celsius`, which *is* the property, so the setter calls itself forever.

**Fix:** assign to the backing attribute — `self._celsius = value`. The getter already reads `_celsius`, so the names must differ.

`__init__` did not bypass it because attribute assignment always goes through the type's data descriptors. `self.celsius = celsius` in `__init__` is a *feature* here — it means construction gets the same validation as later writes.

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
