"""Problem 07 — Evaluate Reverse Polish Notation

Pattern:    Stack
Difficulty: Medium
Target:     Time O(n), Space O(n)

Evaluate an arithmetic expression in reverse Polish notation. Valid operators
are ``+``, ``-``, ``*`` and ``/``. Division **truncates toward zero**.

Raise ``ValueError`` on a malformed expression.

Constraints
- ``1 <= len(tokens) <= 10**4``
- integer operands, possibly negative

Example:
    >>> eval_rpn(["2", "1", "+", "3", "*"])
    9
    >>> eval_rpn(["4", "13", "5", "/", "+"])
    6

Hints — read one at a time, and try again between each.

    Hint 1: Postfix notation is a stack evaluation: operands go on, an operator takes the top two off and pushes the result.
    Hint 2: Operand order matters for - and /: the SECOND value popped is the left-hand operand.
    Hint 3: Python's // floors toward negative infinity, so -7 // 2 is -4, not -3. Use int(a / b) or int(operator.truediv(a, b)) for truncation toward zero. This is the bug this problem exists to catch.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p07
"""

from __future__ import annotations


def eval_rpn(tokens: list[str]) -> int:
    raise NotImplementedError("implement eval_rpn")
