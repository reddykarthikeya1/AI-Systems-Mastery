"""Problem 02 - Longest Prefix That Is Also a Suffix

Pattern:    KMP prefix function
Difficulty: Medium
Target:     Time O(n), Space O(n)

Return the longest *proper* prefix of ``s`` that is also a suffix
of ``s``. Return the empty string if there is none.

Constraints
- ``1 <= len(s) <= 10**5``

Example
    longest_happy_prefix("level")   -> "l"
    longest_happy_prefix("ababab")  -> "abab"
    longest_happy_prefix("abcdef")  -> ""

Once you have the prefix table this is one line. That is the point of the
exercise: recognising that a problem phrased about prefixes and suffixes is
already solved by a table you know how to build.

Example:
    >>> longest_happy_prefix("level")
    'l'
    >>> longest_happy_prefix("abcdef")
    ''

Hints - read one at a time, and try again between each.

    Hint 1: You already wrote the tool for this in problem 01.
    Hint 2: The last entry of the prefix table is exactly the length of the answer.
    Hint 3: `s[:pi[-1]]`. Be careful with a string of length 1, whose answer is always empty.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def longest_happy_prefix(s: str) -> str:
    raise NotImplementedError("implement longest_happy_prefix")
