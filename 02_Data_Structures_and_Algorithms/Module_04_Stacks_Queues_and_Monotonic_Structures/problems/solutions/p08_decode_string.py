"""Reference solution — Problem 08: Decode String

Pattern:    Stack of contexts
Complexity: Time O(output length), Space O(depth + output)
"""

from __future__ import annotations


def decode_string(s: str) -> str:
    stack: list[tuple[str, int]] = []
    current = ""
    count = 0

    for ch in s:
        if ch.isdigit():
            # Multi-digit counts: "12[a]" must be 12, not 1 then 2.
            count = count * 10 + int(ch)
        elif ch == "[":
            stack.append((current, count))
            current, count = "", 0
        elif ch == "]":
            if not stack:
                raise ValueError("unbalanced ']' in encoded string")
            prev_text, repeat = stack.pop()
            current = prev_text + current * repeat
        else:
            current += ch

    if stack:
        raise ValueError("unbalanced '[' in encoded string")
    return current
