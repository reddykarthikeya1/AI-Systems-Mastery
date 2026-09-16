# Module 23: Self-Assessment Quiz & Mastery Challenges

Test your understanding of Strict Typing, Protocols, Mypy, and Modern Packaging before moving to **Module 22**.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Nominal vs Structural:** What is the technical difference between Nominal Subtyping (standard inheritance) and Structural Subtyping (`typing.Protocol`)?
2. **Generics:** What is the purpose of `TypeVar("T")` and `Generic[T]` when designing reusable data structures?
3. **Decorator Typing:** How does `typing.ParamSpec` preserve the exact parameter signature of a decorated function?
4. **The Type Marker:** What is the purpose of the `py.typed` file in a published Python package?
5. **Circular Imports:** How does `if typing.TYPE_CHECKING:` resolve runtime circular dependency errors?
6. **Deferred Annotations:** What does `from __future__ import annotations` (PEP 563) do to type expressions at module load time?
7. **PEP 621 Standard:** What standard did PEP 621 establish for `pyproject.toml` metadata?
8. **Fluent APIs:** What typing feature in Python 3.11+ simplifies typing method chaining (`return self`) across inheritance hierarchies?
9. **Type Narrowing:** What is `typing.TypeGuard`, and how does it help type checkers narrow down ambiguous types?
10. **Build Backends:** Name two modern build backends supported by `pyproject.toml` instead of legacy `setup.py`.

---

## Part 2: Answer Key & Explanations

<details>
<summary><b>Click to expand the Answer Key & Detailed Explanations</b></summary>

#### Answer 1:
- **Nominal:** Types must explicitly inherit from a parent class (`class Dog(Animal):`).
- **Structural (Duck Typing):** An object matches the type if it possesses the required methods and attributes, without explicit inheritance.

#### Answer 2:
It allows classes and functions to operate over arbitrary data types while strictly preserving type identity between inputs and outputs.

#### Answer 3:
`ParamSpec` captures the exact positional and keyword arguments of a callable `Callable[P, R]`, ensuring full type safety through decorators.

#### Answer 4:
It informs type checkers (Mypy, Pyright) that the installed package ships with inline type annotations that should be statically analyzed.

#### Answer 5:
`TYPE_CHECKING` evaluates to `False` at runtime (bypassing the import) and `True` only during static type checking.

#### Answer 6:
It turns type hints into inert string literals rather than evaluating them at runtime, eliminating forward reference errors and speeding up import time.

#### Answer 7:
It standardized package metadata (`[project]` table with name, version, authors, dependencies) into a universal declarative format.

#### Answer 8:
**`typing.Self`** (PEP 673).

#### Answer 9:
A custom boolean function return annotation (`def is_user(val) -> TypeGuard[User]`) that informs the type checker that the inspected variable is definitely of that type when `True`.

#### Answer 10:
**`hatchling`** and **`flit_core`**.

</details>

---

## Part 3: Practical Coding Challenges

### Challenge 1: Type-Safe Generic Stack

**Goal:** Implement a generic `Stack[T]` with `push(item: T) -> None` and `pop() -> T`.

<details>
<summary><b>Solution Code</b></summary>

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

# Verification:
s = Stack[int]()
s.push(10)
s.push(20)
print("Popped item:", s.pop())
```
</details>

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. `Any` silently defeats the type checker

```python
from typing import Any

def load(raw: Any) -> int:
    return raw["count"] + 1        # mypy reports no error
```

**Observed symptom:** `mypy --strict` passes. Production raises `TypeError: string indices must be integers`.

**(a)** Why does mypy not complain?

**(b)** What should the parameter be typed as?

**(c)** How do you stop `Any` creeping in unnoticed?

<details>
<summary><b>Show the diagnosis</b></summary>

`Any` is **compatible with everything in both directions**. Every operation on an `Any` value type-checks, and the result is also `Any`, so the error propagates silently through the rest of the function.

**Type it as** `object` if you truly do not know (then mypy *forces* you to narrow before use), or better a `TypedDict`:

```python
class Payload(TypedDict):
    count: int
```

which gives you key checking and value types.

**Stop the creep** with `disallow_any_explicit` and `warn_return_any` in the mypy config, and `--disallow-untyped-defs` so an unannotated function cannot quietly become `Any`. Run `mypy --strict` in CI. The distinction to internalise: `Any` disables checking; `object` demands narrowing. Reaching for `Any` to silence an error usually means hiding a real one.

</details>

---

### D2. Protocol not actually satisfied

```python
from typing import Protocol

class Writer(Protocol):
    def write(self, data: bytes) -> int: ...

class Logger:
    def write(self, data: str) -> None:      # str, not bytes; None, not int
        print(data)

def emit(w: Writer, payload: bytes) -> None:
    w.write(payload)

emit(Logger(), b"hello")
```

**Observed symptom:** `mypy` flags it, but the code runs fine in a quick manual test — so the error gets dismissed as a false positive.

**(a)** Name the two incompatibilities.

**(b)** Why is the runtime 'success' misleading?

**(c)** What does `@runtime_checkable` actually check?

<details>
<summary><b>Show the diagnosis</b></summary>

**Two:** the parameter type is `str` where the protocol requires `bytes` (contravariance — an implementation must accept *at least* what the protocol promises), and the return is `None` where `int` is required (covariance).

**Runtime success is misleading** because `print(b'hello')` happens to work — it prints `b'hello'`, which is wrong output, not correct behaviour. And any caller that uses the returned byte count will get `None` and fail somewhere distant. mypy is describing a real defect.

**`@runtime_checkable`** enables `isinstance()` against the protocol, but it checks **only that the attribute names exist** — not their signatures or types. `isinstance(Logger(), Writer)` returns `True` here. It is a shallow structural check, useful for dispatch, never a substitute for static verification.

</details>

---

### D3. Mutable default in a frozen dataclass

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Config:
    tags: list[str] = field(default_factory=list)

c = Config()
c.tags.append("prod")
print(c.tags)
```

**Observed symptom:** Prints `['prod']` — the 'frozen' object changed.

**(a)** What does `frozen=True` actually prevent?

**(b)** How do you get genuine immutability?

**(c)** What does this break about hashing?

<details>
<summary><b>Show the diagnosis</b></summary>

`frozen=True` blocks **attribute assignment** (`c.tags = [...]` raises `FrozenInstanceError`). It says nothing about mutating the object an attribute *points to*. This is shallow immutability.

**Genuine immutability:** use an immutable type — `tags: tuple[str, ...] = ()`. For a read-only view of a mutable source, `types.MappingProxyType` for dicts. There is no built-in frozen list; a tuple is the answer.

**Hashing:** `frozen=True` generates `__hash__` from the fields, but hashing a `list` field raises `TypeError: unhashable type`. So the class advertises hashability it cannot deliver, and you discover it the first time you put one in a set. With `tuple` the hash works, and — crucially — stays stable, which is the invariant that made hashing safe in the first place (see Module 04's `__eq__`/`__hash__` diagnostic).

</details>

---

### D4. Wheel that installs nowhere

```
$ maturin build --release
$ ls target/wheels/
rust_accelerator-1.0.0-cp312-cp312-win_amd64.whl
```

**Observed symptom:** `pip install` on a colleague's Python 3.11 machine: *is not a supported wheel on this platform*.

**(a)** What does the `cp312-cp312` tag mean?

**(b)** What produces a portable tag, and what is the trade-off?

**(c)** How many builds does each approach need for 3.11-3.14 on 3 platforms?

<details>
<summary><b>Show the diagnosis</b></summary>

`cp312-cp312` means CPython 3.12 ABI specifically. The wheel is bound to one minor version because it uses the version-specific C API.

**Portable tag:** the **stable ABI** — `pyo3 = { features = ["abi3-py311"] }` — which produces `cp311-abi3`, installable on 3.11 and every later version. The trade-off is that you may use only the stable subset of the C API; for the large majority of extensions that is no restriction at all.

**Build count:** without abi3, 4 versions × 3 platforms = **12 builds**, and a 13th the day 3.15 ships. With abi3, **3 builds**, and nothing to do when 3.15 ships. That is the whole argument.

</details>

---

### D5. Type stubs missing for a native module

```python
import rust_accelerator

result: int = rust_accelerator.fnv1a_64(b"data")     # mypy: no error, no checking
```

**Observed symptom:** `mypy --strict` reports `Skipping analyzing "rust_accelerator": module is installed, but missing library stubs or py.typed marker`.

**(a)** Why can mypy not infer types from the compiled module?

**(b)** What two files fix it?

**(c)** What would happen if the stub disagreed with the implementation?

<details>
<summary><b>Show the diagnosis</b></summary>

The module is a compiled `.pyd`/`.so`. There is no Python source to analyse, and the C-level signatures are not introspectable in a form mypy understands, so every call returns `Any`.

**Two files:** a stub file `rust_accelerator.pyi` declaring each signature, and an empty `py.typed` marker in the package so type checkers know to trust the inline/stub types (PEP 561).

**A disagreeing stub is worse than no stub** — it makes the type checker confidently wrong, and there is nothing to catch it, because the stub *is* the source of truth for static analysis. Guard against drift with a runtime test that exercises each function and asserts the returned types, so the stub and the implementation are checked against each other by the suite rather than by hope.

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
