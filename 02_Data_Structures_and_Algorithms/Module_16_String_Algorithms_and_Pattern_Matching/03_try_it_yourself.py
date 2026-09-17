"""Beginner playground for Module 16 - String Algorithms & Pattern Matching.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. KMP Prefix Function (Pi Array)
def compute_pi(pattern: str) -> list[int]:
    pi = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j
    return pi

pi_table = compute_pi("aabaabaaa")
assert pi_table[0] == 0
assert pi_table[1] == 1, "'aa' prefix 'a'"
assert pi_table[4] == 2, "'aabaa' prefix 'aa'"
print(f"KMP Pi table for 'aabaabaaa': {pi_table}")

# -------------------------------------------- 2. KMP Linear-Time Substring Search
def kmp_search(text: str, pattern: str) -> list[int]:
    pi = compute_pi(pattern)
    matches = []
    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == len(pattern):
            matches.append(i - j + 1)
            j = pi[j - 1]
    return matches

hits = kmp_search("sadbutsad", "sad")
assert hits == [0, 6]
assert kmp_search("leetcode", "leeto") == []
print(f"KMP matches found at indices: {hits}")

# -------------------------------------------- 3. Rabin-Karp Rolling Hash Matching
def rolling_hash(s, base=256, mod=1000000007):
    h = 0
    for ch in s:
        h = (h * base + ord(ch)) % mod
    return h

h1 = rolling_hash("apple")
h2 = rolling_hash("apple")
h3 = rolling_hash("apply")
assert h1 == h2
assert h1 != h3
print(f"Rolling hash values: 'apple'={h1}, 'apply'={h3}")

print()
print("All checks passed.")
