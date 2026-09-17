"""Problem 01 — Contextual Exception Chaining

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def format_exception_chain(exc: BaseException) -> list[str]:
    chain = []
    curr = exc
    while curr is not None:
        chain.append(f"{type(curr).__name__}: {str(curr)}")
        curr = curr.__cause__ or curr.__context__
    return chain
