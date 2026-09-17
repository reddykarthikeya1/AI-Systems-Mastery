"""Tests for the string matching engine.

The important ones are differential: every fast algorithm is checked against
`naive_search` on randomised input. An algorithm that agrees with a correct
brute force on ten thousand random cases is almost certainly right, and the
ones that are wrong fail immediately rather than on one input in production.
"""

from __future__ import annotations

import random
import time

import pytest
from string_matching_engine import (
    AhoCorasick,
    RollingHash,
    build_automaton,
    kmp_search,
    naive_search,
    naive_search_char_by_char,
    prefix_function,
    rabin_karp_2d,
    rabin_karp_search,
    rabin_karp_search_unverified,
    smallest_period,
    z_function,
    z_search,
)

ALGORITHMS = [kmp_search, z_search, rabin_karp_search]


# ---------------------------------------------------------------------------
# prefix function
# ---------------------------------------------------------------------------


def test_prefix_function_known_values():
    assert prefix_function("ababaca") == [0, 0, 1, 2, 3, 0, 1]
    assert prefix_function("aaaa") == [0, 1, 2, 3]
    assert prefix_function("abcdef") == [0, 0, 0, 0, 0, 0]
    assert prefix_function("") == []


def test_prefix_function_never_equals_its_own_index():
    # pi[i] < i + 1 always: a proper prefix cannot be the whole string.
    for word in ("aaaaaa", "abcabcabc", "aabaaab"):
        pi = prefix_function(word)
        assert all(value <= index for index, value in enumerate(pi))


def test_smallest_period():
    assert smallest_period("abcabcabc") == 3
    assert smallest_period("aaaa") == 1
    assert smallest_period("abcd") == 4          # no repetition: the whole word
    assert smallest_period("abcabca") == 7       # 3 does not divide 7
    assert smallest_period("") == 0


# ---------------------------------------------------------------------------
# differential testing against the brute force
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("search", ALGORITHMS)
def test_matches_naive_on_random_input(search):
    random.seed(16)
    for _ in range(400):
        alphabet = random.choice(["ab", "abc", "abcdefgh"])
        text = "".join(random.choice(alphabet) for _ in range(random.randint(0, 60)))
        pattern = "".join(random.choice(alphabet) for _ in range(random.randint(1, 6)))
        assert search(text, pattern) == naive_search(text, pattern), (
            f"disagreement on text={text!r} pattern={pattern!r}")


@pytest.mark.parametrize("search", ALGORITHMS)
def test_overlapping_matches_are_all_reported(search):
    # The classic off-by-one: resetting to 0 after a match loses the overlaps.
    assert search("aaaa", "aa") == [0, 1, 2]
    assert search("abababa", "aba") == [0, 2, 4]


@pytest.mark.parametrize("search", ALGORITHMS)
def test_pattern_longer_than_text(search):
    assert search("ab", "abcdef") == []


@pytest.mark.parametrize("search", ALGORITHMS)
def test_pattern_equal_to_text(search):
    assert search("abc", "abc") == [0]


@pytest.mark.parametrize("search", ALGORITHMS)
def test_no_match(search):
    assert search("abcdefgh", "xyz") == []


@pytest.mark.parametrize("search", ALGORITHMS)
def test_empty_text(search):
    assert search("", "a") == []


# ---------------------------------------------------------------------------
# Z-algorithm specifics
# ---------------------------------------------------------------------------


def test_z_function_known_values():
    assert z_function("aaaaa") == [5, 4, 3, 2, 1]
    assert z_function("abacaba") == [7, 0, 1, 0, 3, 0, 1]
    assert z_function("") == []


def test_z_search_rejects_a_separator_that_occurs_in_the_input():
    with pytest.raises(ValueError):
        z_search("a#b", "b", separator="#")


# ---------------------------------------------------------------------------
# rolling hash
# ---------------------------------------------------------------------------


def test_rolling_hash_matches_a_fresh_hash_after_rolling():
    text = "the quick brown fox"
    width = 5
    window = RollingHash(width)
    for character in text[:width]:
        window.push(character)
    for start in range(len(text) - width):
        window.roll(text[start], text[start + width])
        expected = RollingHash.of(text[start + 1:start + 1 + width])
        assert window.value == expected, f"drifted at offset {start + 1}"


def test_unverified_rabin_karp_reports_matches_that_are_not_there():
    """The bug this module exists to make memorable.

    With a small modulus, different strings collide. Trusting the hash reports
    a match at an offset where the text does not contain the pattern at all.
    """
    random.seed(7)
    text = "".join(random.choice("abcdefgh") for _ in range(4_000))
    pattern = "abc"

    truth = naive_search(text, pattern)
    unverified = rabin_karp_search_unverified(text, pattern, mod=101)

    false_positives = [i for i in unverified if i not in truth]
    assert false_positives, "expected collisions with such a small modulus"
    bad = false_positives[0]
    assert text[bad:bad + len(pattern)] != pattern
    # And the verified version is exactly right on the same input.
    assert rabin_karp_search(text, pattern) == truth


# ---------------------------------------------------------------------------
# 2-D Rabin-Karp
# ---------------------------------------------------------------------------


def test_rabin_karp_2d_finds_a_block():
    grid = [
        "abcdef",
        "ghijkl",
        "mnopqr",
        "stuvwx",
    ]
    assert rabin_karp_2d(grid, ["hij", "nop"]) == [(1, 1)]
    assert rabin_karp_2d(grid, ["abc"]) == [(0, 0)]
    assert rabin_karp_2d(grid, ["zz"]) == []


def test_rabin_karp_2d_finds_every_occurrence():
    grid = ["aaaa", "aaaa", "aaaa"]
    found = rabin_karp_2d(grid, ["aa", "aa"])
    assert found == [(row, col) for row in range(2) for col in range(3)]


def test_rabin_karp_2d_pattern_larger_than_grid():
    assert rabin_karp_2d(["ab"], ["abc"]) == []
    assert rabin_karp_2d(["ab"], ["ab", "cd"]) == []


# ---------------------------------------------------------------------------
# Aho-Corasick
# ---------------------------------------------------------------------------


def test_aho_corasick_finds_overlapping_and_nested_patterns():
    automaton = build_automaton(["he", "she", "his", "hers"])
    hits = automaton.search("ushers")
    # "she" ends at 3, "he" ends at 3 (nested inside it), "hers" ends at 5.
    assert ("she", 3) in [(w, i) for i, w in hits]
    assert ("he", 3) in [(w, i) for i, w in hits]
    assert ("hers", 5) in [(w, i) for i, w in hits]


def test_aho_corasick_agrees_with_running_naive_per_pattern():
    random.seed(161)
    for _ in range(120):
        patterns = list({
            "".join(random.choice("abc") for _ in range(random.randint(1, 4)))
            for _ in range(random.randint(1, 5))
        })
        text = "".join(random.choice("abc") for _ in range(random.randint(0, 80)))

        expected = set()
        for word in patterns:
            for start in naive_search(text, word):
                expected.add((start + len(word) - 1, word))

        assert set(build_automaton(patterns).search(text)) == expected


def test_aho_corasick_rejects_the_empty_pattern():
    automaton = AhoCorasick()
    with pytest.raises(ValueError):
        automaton.add("")


def test_aho_corasick_requires_build_before_search():
    automaton = AhoCorasick()
    automaton.add("abc")
    with pytest.raises(RuntimeError):
        automaton.search("abc")


def test_aho_corasick_rejects_add_after_build():
    automaton = build_automaton(["abc"])
    with pytest.raises(RuntimeError):
        automaton.add("def")


def test_contains_any_short_circuits():
    screen = build_automaton(["badword", "worse"])
    assert screen.contains_any("this contains badword here")
    assert not screen.contains_any("this one is entirely fine")


# ---------------------------------------------------------------------------
# scale: the whole reason these algorithms exist
# ---------------------------------------------------------------------------


@pytest.mark.perf
def test_kmp_beats_the_naive_algorithm_on_the_pathological_input():
    """The input that makes the naive scan quadratic.

    "aaaa...aab" against "aaa...ab": every offset matches almost to the end
    before failing on the last character, so naive re-reads the whole pattern
    at every one of the n offsets. KMP never moves the text pointer backwards.

    The baseline here is the char-by-char version deliberately. Comparing
    against the slice-based one measures C against Python, not algorithm
    against algorithm - see the next test.
    """
    text = "a" * 5_000 + "b"
    pattern = "a" * 500 + "b"

    start = time.perf_counter()
    naive = naive_search_char_by_char(text, pattern)
    naive_seconds = time.perf_counter() - start

    start = time.perf_counter()
    fast = kmp_search(text, pattern)
    kmp_seconds = time.perf_counter() - start

    assert naive == fast == [4_500]
    assert kmp_seconds < naive_seconds / 10, (
        f"KMP {kmp_seconds * 1000:.1f} ms vs naive {naive_seconds * 1000:.1f} ms")


@pytest.mark.perf
def test_the_constant_factor_erases_the_asymptotic_advantage():
    """The result a complexity table will not tell you, asserted.

    `naive_search` is O(n*m) but its inner comparison is a C memcmp.
    `kmp_search` is O(n + m) but every step is Python bytecode.

    On this input the asymptotic work ratio is (n*m)/(n+m), about 1,800 - so
    reading big-O as a prediction of runtime says naive should take roughly
    1,800 times longer. Measured, the two are within a small factor of each
    other, and which one wins moves with the machine and the Python build.

    The test asserts the robust part: the measured ratio is nowhere near what
    the asymptotics alone predict. That gap IS the constant factor, and it is
    why `in` and `str.find` beat a hand-written matcher far more often than
    complexity classes suggest.
    """
    text = "a" * 20_000 + "b"
    pattern = "a" * 2_000 + "b"
    n, m = len(text), len(pattern)
    predicted_ratio = (n * m) / (n + m)

    start = time.perf_counter()
    quadratic_in_c = naive_search(text, pattern)
    c_seconds = time.perf_counter() - start

    start = time.perf_counter()
    linear_in_python = kmp_search(text, pattern)
    python_seconds = time.perf_counter() - start

    measured_ratio = c_seconds / python_seconds
    assert quadratic_in_c == linear_in_python == [18_000], "both are correct"
    assert measured_ratio < predicted_ratio / 100, (
        f"asymptotics predict naive is ~{predicted_ratio:.0f}x slower; "
        f"measured {measured_ratio:.2f}x "
        f"(naive {c_seconds * 1000:.1f} ms, KMP {python_seconds * 1000:.1f} ms)")


@pytest.mark.perf
def test_aho_corasick_beats_running_kmp_once_per_pattern():
    """One pass for k patterns, versus k passes.

    The gap grows with the number of patterns, which is exactly the situation a
    content filter is in: thousands of terms, every message.
    """
    random.seed(99)
    text = "".join(random.choice("abcdefgh") for _ in range(60_000))
    patterns = ["".join(random.choice("abcdefgh") for _ in range(5))
                for _ in range(300)]

    start = time.perf_counter()
    for word in patterns:
        kmp_search(text, word)
    kmp_seconds = time.perf_counter() - start

    automaton = build_automaton(patterns)
    start = time.perf_counter()
    automaton.search(text)
    aho_seconds = time.perf_counter() - start

    assert aho_seconds < kmp_seconds, (
        f"Aho-Corasick {aho_seconds * 1000:.0f} ms vs "
        f"{len(patterns)}x KMP {kmp_seconds * 1000:.0f} ms")
def test_kmp_edge_cases():
    # Pattern longer than text
    assert kmp_search("short", "longer_pattern_here") == []
    # Pattern equals text
    assert kmp_search("exact", "exact") == [0]
    # Character not in text
    assert kmp_search("abcdef", "z") == []
    # Overlapping matches
    assert kmp_search("AAAAA", "AAA") == [0, 1, 2]


def test_prefix_and_z_function_edge_cases():
    assert prefix_function("") == []
    assert prefix_function("a") == [0]
    assert prefix_function("aaaa") == [0, 1, 2, 3]
    assert prefix_function("abcd") == [0, 0, 0, 0]
    
    assert z_function("") == []
    assert z_function("a") == [1]
    assert z_function("aaaa") == [4, 3, 2, 1]
