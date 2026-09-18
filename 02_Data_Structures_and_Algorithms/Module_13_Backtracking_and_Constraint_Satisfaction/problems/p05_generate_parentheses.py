"""Problem 05 — Generate Valid Parentheses

Pattern:    Backtracking with validity pruning
Difficulty: Medium
Target:     Time O(4^n / sqrt(n)) (Catalan), Space O(n)

Return every well-formed string of ``n`` pairs of parentheses, sorted.

Constraints
- ``0 <= n <= 8``

Example
    generate_parentheses(3)
    -> ["((()))", "(()())", "(())()", "()(())", "()()()"]

Example:
    >>> generate_parentheses(3)
    ['((()))', '(()())', '(())()', '()(())', '()()()']

Hints — read one at a time, and try again between each.

    Hint 1: Generating all 2^(2n) strings and filtering works but wastes almost all of the work.
    Hint 2: Instead only ever build valid prefixes: you may add '(' while you have used fewer than n, and ')' only while it would not exceed the number of '(' already placed.
    Hint 3: That single condition prunes every invalid branch before it grows, which is what makes this fast rather than merely correct.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def generate_parentheses(n: int) -> list[str]:
    raise NotImplementedError("implement generate_parentheses")
