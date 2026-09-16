"""Problem 01 — Valid Parentheses

Pattern:    Stack
Difficulty: Easy
Target:     Time O(n), Space O(n)

Return True if every bracket in ``s`` is closed by the same type, in the correct
order. The string contains only ``()[]{}``.

Constraints
- ``0 <= len(s) <= 10**4``

Example
    "()[]{}"  -> True
    "([)]"    -> False
    "("       -> False

Hints — read one at a time, and try again between each.

    Hint 1: Nested structure is the signal for a stack.
    Hint 2: Push opening brackets. On a closing bracket, the top of the stack must be its matching opener.
    Hint 3: Two failure cases to remember: a closing bracket with an empty stack, and a non-empty stack at the very end.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def balanced_brackets(s: str) -> bool:
    raise NotImplementedError("implement balanced_brackets")
