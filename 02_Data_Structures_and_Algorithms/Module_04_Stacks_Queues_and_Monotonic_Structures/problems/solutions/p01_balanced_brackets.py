"""Reference solution — Problem 01: Valid Parentheses

Pattern:    Stack
Complexity: Time O(n), Space O(n)
"""

from __future__ import annotations


def balanced_brackets(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []

    for ch in s:
        if ch in pairs:
            # A closer with nothing open, or the wrong opener on top.
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)

    # Anything still open is unbalanced.
    return not stack
