"""Problem 01 — Trie: Insert, Search, StartsWith

Pattern:    Trie
Difficulty: Medium
Target:     Time O(len(word)) per operation, Space O(total characters)

Simulate a trie supporting ``insert``, ``search`` (exact word) and
``starts_with`` (any word with this prefix).

``ops`` is a list of ``(operation, argument)`` pairs. Return the boolean result
of each ``search`` and ``starts_with``, in order; ``insert`` returns nothing.

Constraints
- ``1 <= len(ops) <= 10**4``
- lowercase words

Example
    ops = [("insert","apple"), ("search","apple"), ("search","app"),
           ("starts_with","app"), ("insert","app"), ("search","app")]
    -> [True, False, True, True]

Hints — read one at a time, and try again between each.

    Hint 1: A trie node is just a mapping from a character to a child node, plus a flag saying whether a word ends here.
    Hint 2: The end-of-word flag is what distinguishes `search` from `starts_with`. Without it you cannot tell 'app' the word from 'app' the prefix.
    Hint 3: Both operations walk the prefix identically; they differ only in what they check at the node they land on.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def simulate_trie(ops: list[tuple[str, str]]) -> list[bool | None]:
    raise NotImplementedError("implement simulate_trie")
