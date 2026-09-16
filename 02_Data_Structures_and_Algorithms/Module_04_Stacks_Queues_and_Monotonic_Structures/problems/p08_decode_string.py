"""Problem 08 — Decode String

Pattern:    Stack of contexts
Difficulty: Medium
Target:     Time O(output length), Space O(depth + output)

Decode a string encoded as ``k[substring]``, meaning the substring repeated
``k`` times. Encodings nest.

Constraints
- ``1 <= len(s) <= 30``
- digits appear only as repeat counts, and ``k >= 1``; ``k`` may be multi-digit

Example
    "3[a]2[bc]"   -> "aaabcbc"
    "3[a2[c]]"    -> "accaccacc"
    "2[abc]3[cd]ef" -> "abcabccdcdcdef"

Hints — read one at a time, and try again between each.

    Hint 1: Nesting is the signal for a stack. What has to be remembered when you enter a bracket?
    Hint 2: Two things: the text built so far, and the repeat count that applies to what comes next.
    Hint 3: On '[' push (current_text, count) and reset both. On ']' pop them and set current = previous_text + count * current. Accumulate multi-digit counts with count = count * 10 + digit.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p08
"""

from __future__ import annotations


def decode_string(s: str) -> str:
    raise NotImplementedError("implement decode_string")
