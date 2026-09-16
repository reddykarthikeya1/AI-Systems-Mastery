"""Problem-bank suite for Module_16_String_Algorithms_and_Pattern_Matching.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs - which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import random
import time

from p01_prefix_table import build_prefix_table
from p02_longest_happy_prefix import longest_happy_prefix
from p03_repeated_pattern import is_repeated_pattern
from p04_shortest_palindrome import shortest_palindrome
from p05_find_all_occurrences import find_all
from p06_censor_dictionary import censor


def test_p01_prefix_table():
    """Build the KMP Prefix Table - KMP prefix function (Medium)."""
    assert build_prefix_table("ababaca") == [0, 0, 1, 2, 3, 0, 1]
    assert build_prefix_table("aaaa") == [0, 1, 2, 3]
    assert build_prefix_table("abcdef") == [0, 0, 0, 0, 0, 0]
    # Empty and single character: the boundary everyone forgets.
    assert build_prefix_table("") == []
    assert build_prefix_table("a") == [0]
    # pi[i] can never exceed i - a proper prefix is not the whole string.
    for word in ("aabaabaaa", "abacabadabacaba"):
        assert all(v <= i for i, v in enumerate(build_prefix_table(word)))


def test_p02_longest_happy_prefix():
    """Longest Prefix That Is Also a Suffix - KMP prefix function (Medium)."""
    assert longest_happy_prefix("level") == "l"
    assert longest_happy_prefix("ababab") == "abab"
    assert longest_happy_prefix("abcdef") == ""
    assert longest_happy_prefix("a") == ""
    assert longest_happy_prefix("aa") == "a"
    # Must be a PROPER prefix: never the whole string.
    for word in ("aaaa", "abab", "xyzxyz"):
        assert len(longest_happy_prefix(word)) < len(word)


def test_p03_repeated_pattern():
    """Is the String a Repeated Block? - String period (Medium)."""
    assert is_repeated_pattern("abab")
    assert is_repeated_pattern("abcabcabc")
    assert is_repeated_pattern("aaaa")
    assert not is_repeated_pattern("aba")
    assert not is_repeated_pattern("a")
    assert not is_repeated_pattern("abcabca")   # period 3 does not divide 7
    assert not is_repeated_pattern("abaababaab" + "x")
    # Cross-check against the obvious O(n^2) definition.
    random.seed(1601)
    for _ in range(300):
        s = "".join(random.choice("ab") for _ in range(random.randint(1, 12)))
        expected = any(len(s) % k == 0 and s[:k] * (len(s) // k) == s
                       for k in range(1, len(s)))
        assert is_repeated_pattern(s) == expected, s


def test_p04_shortest_palindrome():
    """Shortest Palindrome by Prepending - KMP on s + sep + reversed(s) (Hard)."""
    assert shortest_palindrome("aacecaaa") == "aaacecaaa"
    assert shortest_palindrome("abcd") == "dcbabcd"
    assert shortest_palindrome("") == ""
    assert shortest_palindrome("a") == "a"
    assert shortest_palindrome("aa") == "aa"
    assert shortest_palindrome("aba") == "aba"     # already a palindrome
    # The result must be a palindrome, must end with s, and must be minimal.
    random.seed(1604)
    for _ in range(200):
        s = "".join(random.choice("ab") for _ in range(random.randint(0, 10)))
        out = shortest_palindrome(s)
        assert out == out[::-1], f"{s!r} -> {out!r} is not a palindrome"
        assert out.endswith(s), f"{s!r} -> {out!r} does not end with the input"
        keep = max(k for k in range(len(s) + 1) if s[:k] == s[:k][::-1])
        brute = s[keep:][::-1] + s
        assert out == brute, f"{s!r}: got {out!r}, shortest is {brute!r}"


def test_p05_find_all_occurrences():
    """All Occurrences, Overlaps Included - Linear-time string search (Medium)."""
    assert find_all("aaaa", "aa") == [0, 1, 2]
    assert find_all("abababa", "aba") == [0, 2, 4]
    assert find_all("abc", "") == []
    assert find_all("", "a") == []
    assert find_all("abc", "abcd") == []
    assert find_all("abc", "abc") == [0]
    # Differential against a plain scan.
    random.seed(1605)
    for _ in range(400):
        text = "".join(random.choice("ab") for _ in range(random.randint(0, 40)))
        pattern = "".join(random.choice("ab") for _ in range(random.randint(1, 4)))
        expected = [i for i in range(len(text) - len(pattern) + 1)
                    if text[i:i + len(pattern)] == pattern]
        assert find_all(text, pattern) == expected


def test_p05_find_all_is_linear():
    """The adversarial input. A quadratic scan cannot finish this in time."""
    text = "a" * 50_000 + "b"
    pattern = "a" * 1_000 + "b"
    start = time.perf_counter()
    assert find_all(text, pattern) == [49_000]
    assert time.perf_counter() - start < 2.0, "O(n*m) will not make this budget"


def test_p06_censor_dictionary():
    """Censor Every Banned Term in One Pass - Aho-Corasick (Hard)."""
    assert censor("ushers", ["he", "she"]) == "u***rs"
    assert censor("hello world", ["world"]) == "hello *****"
    assert censor("abc", []) == "abc"
    assert censor("", ["a"]) == ""
    assert censor("abc", [""]) == "abc"
    # Nested terms: the shorter one inside the longer must also be covered.
    assert censor("shisher", ["his", "she", "he"]) == "s*****r"
    # Nothing to censor leaves the text untouched.
    assert censor("clean text", ["zzz"]) == "clean text"
    # Differential against the obvious slow version.
    random.seed(1606)
    for _ in range(200):
        text = "".join(random.choice("abc") for _ in range(random.randint(0, 30)))
        banned = list({"".join(random.choice("abc") for _ in range(random.randint(1, 3)))
                       for _ in range(random.randint(0, 4))})
        flags = [False] * len(text)
        for word in banned:
            for i in range(len(text) - len(word) + 1):
                if text[i:i + len(word)] == word:
                    for j in range(i, i + len(word)):
                        flags[j] = True
        expected = "".join("*" if f else c for c, f in zip(text, flags, strict=True))
        assert censor(text, banned) == expected


def test_p06_censor_is_one_pass():
    """1,000 banned terms over a long text. Searching once per term is O(k*n)."""
    random.seed(1607)
    text = "".join(random.choice("abcdefgh") for _ in range(40_000))
    banned = list({"".join(random.choice("abcdefgh") for _ in range(6))
                   for _ in range(1_000)})
    start = time.perf_counter()
    out = censor(text, banned)
    assert len(out) == len(text)
    assert time.perf_counter() - start < 5.0, "one automaton, one pass"
