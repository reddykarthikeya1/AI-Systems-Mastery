"""Problem 08 — Word Ladder Length

Pattern:    BFS over an implicit graph
Difficulty: Hard
Target:     Time O(N * L * 26), Space O(N * L)

Transform ``begin`` into ``end`` one letter at a time, where every intermediate
word must be in ``word_list``. Return the number of words in the shortest such
sequence, including both ends, or ``0`` if impossible.

``begin`` need not be in ``word_list``; ``end`` must be.

Constraints
- ``1 <= len(word) <= 10``, ``1 <= len(word_list) <= 5000``
- all words the same length, lowercase

Example
    word_ladder("hit", "cog", ["hot","dot","dog","lot","log","cog"]) -> 5
    word_ladder("hit", "cog", ["hot","dot","dog","lot","log"])       -> 0

Hints — read one at a time, and try again between each.

    Hint 1: The graph is implicit: words are nodes, and an edge joins words that differ in exactly one position. Shortest path, unweighted -> BFS.
    Hint 2: Do not compare every pair of words to build the edges - that is O(N^2 * L). Instead, from a word generate its neighbours by trying all 26 letters at each position and checking membership in a set.
    Hint 3: That is O(L * 26) per word. Remove words from the unvisited set as you enqueue them, which both marks them visited and shrinks the work.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p08
"""

from __future__ import annotations


def word_ladder(begin: str, end: str, word_list: list[str]) -> int:
    raise NotImplementedError("implement word_ladder")
