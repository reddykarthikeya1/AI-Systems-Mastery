"""Module 16: watch the prefix table being built, one character at a time.

    python 03_try_it_yourself.py
"""
from __future__ import annotations


def prefix_table_verbose(pattern: str) -> list[int]:
    pi = [0] * len(pattern)
    k = 0
    print(f"  building the table for {pattern!r}")
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            print(f"    i={i} {pattern[i]!r} != {pattern[k]!r}: "
                  f"fall back from k={k} to k={pi[k - 1]}")
            k = pi[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
            print(f"    i={i} {pattern[i]!r} extends the match: k={k}")
        pi[i] = k
    return pi


def search_verbose(text: str, pattern: str) -> list[int]:
    pi = prefix_table_verbose(pattern)
    print(f"  table: {pi}")
    found, k = [], 0
    for i, character in enumerate(text):
        while k > 0 and character != pattern[k]:
            k = pi[k - 1]
        if character == pattern[k]:
            k += 1
        if k == len(pattern):
            found.append(i - len(pattern) + 1)
            k = pi[k - 1]
    return found


def main() -> None:
    print("=" * 62)
    print("DEMO 1: the prefix table")
    print("=" * 62)
    assert prefix_table_verbose("ababaca") == [0, 0, 1, 2, 3, 0, 1]

    print()
    print("=" * 62)
    print("DEMO 2: overlapping matches")
    print("=" * 62)
    result = search_verbose("aaaa", "aa")
    print(f"  'aa' in 'aaaa' -> {result}")
    assert result == [0, 1, 2], "matches overlap - most people predict 2"

    print()
    print("=" * 62)
    print("DEMO 3: a hash match is not a match")
    print("=" * 62)
    mod = 101
    pairs = [(a, b) for a in ("abc", "xyz", "hij") for b in ("qrs", "tuv", "lmn")]
    for a, b in pairs:
        ha = sum(ord(c) * 257 ** (2 - i) for i, c in enumerate(a)) % mod
        hb = sum(ord(c) * 257 ** (2 - i) for i, c in enumerate(b)) % mod
        if ha == hb:
            print(f"  {a!r} and {b!r} both hash to {ha} - and are not equal")
            break
    else:
        print("  no collision in this small sample; widen it and you will find one")

    print()
    print("All demos complete.")


if __name__ == "__main__":
    main()
