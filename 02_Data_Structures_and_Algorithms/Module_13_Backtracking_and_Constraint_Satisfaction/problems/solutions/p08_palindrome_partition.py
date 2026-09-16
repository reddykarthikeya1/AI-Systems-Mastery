"""Reference solution — Problem 08: Palindrome Partitioning

Pattern:    Backtracking with a validity check
Complexity: Time O(n * 2^n), Space O(n) excluding output
"""

from __future__ import annotations


def palindrome_partition(s: str) -> list[list[str]]:
    out: list[list[str]] = []
    path: list[str] = []

    def is_palindrome(text: str) -> bool:
        return text == text[::-1]

    def backtrack(start: int) -> None:
        if start == len(s):
            out.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            # The palindrome test IS the pruning: an invalid prefix cannot lead
            # to a valid partition, so the branch never grows.
            if not is_palindrome(piece):
                continue
            path.append(piece)
            backtrack(end)
            path.pop()

    backtrack(0)
    return sorted(out)
