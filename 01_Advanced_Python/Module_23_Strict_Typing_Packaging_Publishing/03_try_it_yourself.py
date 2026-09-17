"""Beginner playground for Module 23 - Strict Typing & Packaging.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

# -------------------------------------------- 1. Structural Subtyping with Protocol
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

# -------------------------------------------- 2. Type Narrowing with TypeGuard / isinstance
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

# -------------------------------------------- 3. Generic Type Variable Parameterization
from typing import TypeVar, List
T = TypeVar("T")

def first_element(items: List[T]) -> T:
    assert len(items) > 0
    return items[0]

assert first_element([10, 20, 30]) == 10
assert first_element(["x", "y", "z"]) == "x"
print("Generic first_element preserved element values.")

print()
print("All checks passed.")
