"""Problem 06 - Censor Every Banned Term in One Pass

Pattern:    Aho-Corasick
Difficulty: Hard
Target:     Time O(n + total + hits), Space O(total)

Replace every occurrence of every banned word in ``text`` with
``*`` characters, one per censored character. Occurrences may overlap and may
be nested inside one another; every character covered by any banned word is
censored.

Constraints
- ``0 <= len(text) <= 10**5``
- ``0 <= len(banned) <= 10**3``, total banned length ``<= 10**4``
- Running a search once per banned word is O(k*n) and will time out

Example
    censor("ushers", ["he", "she"])   -> "u***rs"
    censor("hello world", ["world"])  -> "hello *****"
    censor("abc", [])                 -> "abc"

Note the first example: `she` covers indices 1-3 and `he` covers 2-3, so the
union is 1-3 - the leading `u` and the trailing `rs` survive. Get the nesting
right, and count the indices rather than trusting your eye.

Example:
    >>> censor("ushers", ["he", "she"])
    'u***rs'
    >>> censor("hello world", ["world"])
    'hello *****'

Hints - read one at a time, and try again between each.

    Hint 1: Build one automaton from all the banned words: a trie plus failure links pointing at the longest proper suffix that is still a node.
    Hint 2: A node must report not only the word ending there but every banned word that is a suffix of it - merge output sets along the failure links as you build, breadth-first.
    Hint 3: Do not edit the string as you go. Mark a boolean array of censored positions first, then build the result in one pass.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def censor(text: str, banned: list[str]) -> str:
    raise NotImplementedError("implement censor")
