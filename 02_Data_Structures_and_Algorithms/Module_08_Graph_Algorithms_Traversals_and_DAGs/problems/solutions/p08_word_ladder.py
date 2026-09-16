"""Reference solution — Problem 08: Word Ladder Length

Pattern:    BFS over an implicit graph
Complexity: Time O(N * L * 26), Space O(N * L)
"""

from __future__ import annotations


def word_ladder(begin: str, end: str, word_list: list[str]) -> int:
    from collections import deque

    remaining = set(word_list)
    if end not in remaining:
        return 0
    remaining.discard(begin)

    queue: deque[tuple[str, int]] = deque([(begin, 1)])
    letters = "abcdefghijklmnopqrstuvwxyz"

    while queue:
        word, length = queue.popleft()
        if word == end:
            return length
        # Generate neighbours instead of comparing all pairs: O(L * 26) rather
        # than O(N * L) per word.
        for i in range(len(word)):
            for ch in letters:
                if ch == word[i]:
                    continue
                candidate = word[:i] + ch + word[i + 1 :]
                if candidate in remaining:
                    remaining.remove(candidate)   # marks visited on enqueue
                    queue.append((candidate, length + 1))

    return 0
