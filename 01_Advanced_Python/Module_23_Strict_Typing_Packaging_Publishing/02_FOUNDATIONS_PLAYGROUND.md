# 🐣 Interactive Foundations Playground: Strict Typing & Packaging

> *"Type protocols define structural subtyping, decoupling interface from implementation."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
from typing import Protocol, runtime_checkable
```

---

## 1. Structural Subtyping with Protocol

`@runtime_checkable Protocol` allows duck-typed structural matching using `isinstance`.

```python
@runtime_checkable
class Renderable(Protocol):
    def render(self) -> str: ...

class MarkdownReport:
    def render(self) -> str:
        return "# Report Content"

class RawText:
    pass

rep = MarkdownReport()
assert isinstance(rep, Renderable)
assert not isinstance(RawText(), Renderable)
assert rep.render() == "# Report Content"
print("Structural typing protocol verified at runtime.")
```

---

## 2. Type Narrowing with TypeGuard / isinstance

Runtime inspection acts as a type guard for narrowing heterogeneous types.

```python
def process_item(item):
    if isinstance(item, int):
        return item * 2
    elif isinstance(item, str):
        return item.upper()
    return None

assert process_item(10) == 20
assert process_item("abc") == "ABC"
assert process_item([1, 2]) is None
print("Runtime type narrowing dispatched correctly.")
```

---

## 3. Generic Type Variable Parameterization

`TypeVar` parameterizes reusable container functions while preserving return types.

```python
from typing import TypeVar, List
T = TypeVar("T")

def first_element(items: List[T]) -> T:
    assert len(items) > 0
    return items[0]

assert first_element([10, 20, 30]) == 10
assert first_element(["x", "y", "z"]) == "x"
print("Generic first_element preserved element values.")
```

---
