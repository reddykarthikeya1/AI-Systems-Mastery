"""Reference solution — Problem 05: Generate Valid Parentheses

Pattern:    Backtracking with validity pruning
Complexity: Time O(4^n / sqrt(n)) (Catalan), Space O(n)
"""

from __future__ import annotations


def generate_parentheses(n: int) -> list[str]:
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    out: list[str] = []
    path: list[str] = []

    def backtrack(opened: int, closed: int) -> None:
        if len(path) == 2 * n:
            out.append("".join(path))
            return
        if opened < n:
            path.append("(")
            backtrack(opened + 1, closed)
            path.pop()
        # Only close what is already open - this prunes every invalid branch
        # before it can grow.
        if closed < opened:
            path.append(")")
            backtrack(opened, closed + 1)
            path.pop()

    backtrack(0, 0)
    return sorted(out)
