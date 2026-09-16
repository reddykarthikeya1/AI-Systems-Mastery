#!/usr/bin/env python3
"""Hash-map utilities. Exits 0, four answers wrong.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

import time

RULE = "=" * 68


def group_anagrams(words: list[str]) -> list[list[str]]:
    buckets: dict[frozenset, list[str]] = {}
    for word in words:
        key = frozenset(word)
        buckets.setdefault(key, []).append(word)
    return sorted(buckets.values(), key=lambda g: g[0])


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    counts: dict[int, int] = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1
    ordered = sorted(counts.items(), key=lambda kv: -kv[1])
    return [value for value, _ in ordered[:k]]


def longest_consecutive(nums: list[int]) -> int:
    present = set(nums)
    best = 0
    for x in present:
        length = 1
        cur = x
        while cur + 1 in present:
            cur += 1
            length += 1
        best = max(best, length)
    return best


def contains_nearby_duplicate(nums: list[int], k: int) -> bool:
    window: set[int] = set()
    for i, x in enumerate(nums):
        if x in window:
            return True
        window.add(x)
    return False


def main() -> None:
    print(RULE)
    print("HASH TOOLKIT")
    print(RULE)

    print()
    print("[1] Anagram grouping")
    cases = [
        ["eat", "tea", "tan", "ate", "nat", "bat"],
        ["aab", "abb"],
        ["ab", "aab", "abb", "aabb"],
    ]
    for words in cases:
        groups = group_anagrams(words)
        print(f"      {words}")
        print(f"          -> {groups}")
        for g in groups:
            canonical = {sorted(w) == sorted(g[0]) for w in g}
            if canonical != {True}:
                print(f"          NOTE: group {g} contains words that are not anagrams")

    print()
    print("[2] Top-k frequent elements")
    for nums, k in (([1, 1, 1, 2, 2, 3], 2), ([3, 2, 1], 2), ([1, 2, 3], 3)):
        print(f"      {nums} k={k} -> {top_k_frequent(nums, k)}")
    print("      (ties must break by ascending value, so [3,2,1] k=2 -> [1, 2])")

    print()
    print("[3] Longest consecutive run (with elapsed time)")
    for nums in ([100, 4, 200, 1, 3, 2], list(range(5_000)), list(range(20_000))):
        label = f"range({len(nums)})" if len(nums) > 10 else str(nums)
        brute = 0
        s = set(nums)
        for v in s:
            if v - 1 not in s:
                n2, ln = v, 1
                while n2 + 1 in s:
                    n2 += 1
                    ln += 1
                brute = max(brute, ln)
        started = time.perf_counter()
        got = longest_consecutive(nums)
        elapsed = (time.perf_counter() - started) * 1000
        print(f"      {label:<16} -> {got:<6} (expected {brute:<6}) "
              f"took {elapsed:9.2f} ms")
    print("      (the input quadrupled from 5000 to 20000 - what did the time do?)")

    print()
    print("[4] Duplicate within distance k")
    for nums, k in (([1, 2, 3, 1], 3), ([1, 2, 3, 1], 2), ([1, 2, 3, 1, 2, 3], 2),
                    ([1, 1], 0)):
        brute = any(
            nums[i] == nums[j]
            for i in range(len(nums))
            for j in range(i + 1, min(len(nums), i + k + 1))
        )
        print(f"      {nums} k={k} -> {contains_nearby_duplicate(nums, k)} "
              f"(expected {brute})")

    print()
    print(RULE)
    print("Toolkit check complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
