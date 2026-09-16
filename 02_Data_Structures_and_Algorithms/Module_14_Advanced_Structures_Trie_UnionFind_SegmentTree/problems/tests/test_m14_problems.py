"""Problem-bank suite for Module_14_Advanced_Structures_Trie_UnionFind_SegmentTree.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import pytest
from p01_trie_operations import simulate_trie
from p02_union_find import simulate_union_find
from p03_segment_tree import simulate_segment_tree
from p04_word_search_trie import words_with_prefix
from p05_accounts_merge import accounts_merge
from p06_range_min_query import range_minimums
from p07_count_smaller_after import count_smaller_after
from p08_implement_prefix_map import simulate_prefix_map


def test_p01_trie_operations():
    """Trie: Insert, Search, StartsWith — Trie (Medium)."""
    ops = [("insert", "apple"), ("search", "apple"), ("search", "app"),
           ("starts_with", "app"), ("insert", "app"), ("search", "app")]
    assert simulate_trie(ops) == [True, False, True, True]
    # Searching an empty trie.
    assert simulate_trie([("search", "a"), ("starts_with", "a")]) == [False, False]
    # The empty prefix always matches once anything exists.
    assert simulate_trie([("insert", "a"), ("starts_with", "")]) == [True]
    # A word is its own prefix.
    assert simulate_trie([("insert", "abc"), ("starts_with", "abc")]) == [True]
    # A longer query than any stored word.
    assert simulate_trie([("insert", "ab"), ("search", "abc")]) == [False]
    # Repeated inserts are idempotent.
    assert simulate_trie([("insert", "x"), ("insert", "x"), ("search", "x")]) == [True]
    with pytest.raises(ValueError):
        simulate_trie([("frobnicate", "x")])
    # Cross-check against a plain set of words on a long sequence.
    import random
    random.seed(11)
    vocab = [''.join(random.choice('abc') for _ in range(random.randint(1, 4))) for _ in range(60)]
    seq, model, expected = [], set(), []
    for _ in range(400):
        w = random.choice(vocab)
        r = random.random()
        if r < 0.4:
            seq.append(('insert', w))
            model.add(w)
        elif r < 0.7:
            seq.append(('search', w))
            expected.append(w in model)
        else:
            seq.append(('starts_with', w))
            expected.append(any(m.startswith(w) for m in model))
    assert simulate_trie(seq) == expected

def test_p02_union_find():
    """Union-Find With Path Compression — Disjoint set union (Medium)."""
    ops = [("connected", 0, 1), ("union", 0, 1), ("connected", 0, 1), ("count", 0, 0)]
    assert simulate_union_find(4, ops) == [False, True, 3]
    # Transitivity: merging 0-1 and 1-2 connects 0 and 2.
    ops = [("union", 0, 1), ("union", 1, 2), ("connected", 0, 2)]
    assert simulate_union_find(3, ops) == [True]
    # A node is connected to itself.
    assert simulate_union_find(1, [("connected", 0, 0), ("count", 0, 0)]) == [True, 1]
    # Redundant unions must not change the count.
    ops = [("union", 0, 1), ("union", 1, 0), ("union", 0, 1), ("count", 0, 0)]
    assert simulate_union_find(3, ops) == [2]
    # Merging everything leaves one set.
    ops = [("union", i, i + 1) for i in range(9)] + [("count", 0, 0)]
    assert simulate_union_find(10, ops) == [1]
    with pytest.raises(ValueError):
        simulate_union_find(2, [("frobnicate", 0, 1)])
    # Scale: 10**5 unions in a chain, which is where a missing path
    # compression turns O(1) into O(n) and this becomes ~10^10 steps.
    big = [("union", i, i + 1) for i in range(99_999)]
    big += [("connected", 0, 99_999), ("count", 0, 0)]
    assert simulate_union_find(100_000, big) == [True, 1]

def test_p03_segment_tree():
    """Segment Tree: Range Sum With Updates — Segment tree (Hard)."""
    assert simulate_segment_tree([1, 3, 5], [("query", 0, 2), ("update", 1, 2), ("query", 0, 2)]) == [9, 8]
    # Single element.
    assert simulate_segment_tree([7], [("query", 0, 0)]) == [7]
    assert simulate_segment_tree([7], [("update", 0, 3), ("query", 0, 0)]) == [3]
    # Sub-ranges and single-element ranges.
    nums = [1, 2, 3, 4, 5]
    ops = [("query", 0, 4), ("query", 1, 3), ("query", 2, 2), ("query", 0, 0)]
    assert simulate_segment_tree(nums, ops) == [15, 9, 3, 1]
    # Negative values.
    assert simulate_segment_tree([-1, -2, 3], [("query", 0, 2)]) == [0]
    with pytest.raises(ValueError):
        simulate_segment_tree([1], [("frobnicate", 0, 0)])
    # Cross-check against a naive model over a long random sequence.
    import random
    random.seed(5)
    base = [random.randint(-50, 50) for _ in range(200)]
    model = base[:]
    seq, expected = [], []
    for _ in range(1500):
        if random.random() < 0.4:
            i, v = random.randrange(len(base)), random.randint(-50, 50)
            seq.append(('update', i, v))
            model[i] = v
        else:
            lo = random.randrange(len(base))
            hi = random.randrange(lo, len(base))
            seq.append(('query', lo, hi))
            expected.append(sum(model[lo : hi + 1]))
    assert simulate_segment_tree(base, seq) == expected

def test_p04_word_search_trie():
    """Find All Dictionary Words With A Prefix — Trie traversal (Medium)."""
    assert words_with_prefix(["cat", "car", "card", "dog"], "car") == ["car", "card"]
    assert words_with_prefix(["cat", "car"], "z") == []
    assert words_with_prefix([], "a") == []
    # The empty prefix returns everything, in order.
    assert words_with_prefix(["b", "a", "c"], "") == ["a", "b", "c"]
    # The limit is honoured.
    assert words_with_prefix(["a", "ab", "abc", "abcd"], "a", limit=2) == ["a", "ab"]
    # A word is its own prefix.
    assert words_with_prefix(["cat"], "cat") == ["cat"]
    # A prefix longer than any word.
    assert words_with_prefix(["cat"], "cats") == []
    # Duplicates collapse.
    assert words_with_prefix(["a", "a"], "a") == ["a"]
    # Cross-check against filtering the list directly.
    vocab = ["apple", "app", "apply", "banana", "band", "bandit", "ban"]
    for pref in ("", "a", "ap", "app", "b", "ban", "z"):
        expected = sorted(w for w in vocab if w.startswith(pref))[:10]
        assert words_with_prefix(vocab, pref) == expected, pref

def test_p05_accounts_merge():
    """Accounts Merge — Union-find over strings (Hard)."""
    got = accounts_merge([
        ["John", "a@x.com", "b@x.com"],
        ["John", "b@x.com", "c@x.com"],
        ["Mary", "m@x.com"],
    ])
    assert got == [["John", "a@x.com", "b@x.com", "c@x.com"], ["Mary", "m@x.com"]]
    # Two DIFFERENT people who happen to share a name must not merge.
    got = accounts_merge([["John", "a@x.com"], ["John", "b@x.com"]])
    assert got == [["John", "a@x.com"], ["John", "b@x.com"]]
    # A single account.
    assert accounts_merge([["A", "a@x.com"]]) == [["A", "a@x.com"]]
    # An account with no emails at all.
    assert accounts_merge([["A"]]) == []
    # A three-way chain merges transitively.
    got = accounts_merge([
        ["A", "1@x.com", "2@x.com"],
        ["A", "2@x.com", "3@x.com"],
        ["A", "3@x.com", "4@x.com"],
    ])
    assert got == [["A", "1@x.com", "2@x.com", "3@x.com", "4@x.com"]]
    # Duplicate emails within one account.
    assert accounts_merge([["A", "a@x.com", "a@x.com"]]) == [["A", "a@x.com"]]
    # Emails must be unique across the output.
    result = accounts_merge([
        ["X", "p@x.com", "q@x.com"], ["Y", "r@x.com"], ["X", "q@x.com", "s@x.com"],
    ])
    flat = [e for acct in result for e in acct[1:]]
    assert len(flat) == len(set(flat))

def test_p06_range_min_query():
    """Sparse Table: Range Minimum, No Updates — Sparse table (Hard)."""
    assert range_minimums([2, 5, 1, 4, 9], [(0, 2), (1, 4), (3, 3)]) == [1, 1, 4]
    # Single element array and single-element ranges.
    assert range_minimums([7], [(0, 0)]) == [7]
    assert range_minimums([3, 1], [(0, 0), (1, 1), (0, 1)]) == [3, 1, 1]
    # The full range.
    assert range_minimums([5, 2, 8], [(0, 2)]) == [2]
    # Negative values.
    assert range_minimums([-1, -5, 3], [(0, 2), (0, 1)]) == [-5, -5]
    # Duplicates.
    assert range_minimums([2, 2, 2], [(0, 2), (1, 2)]) == [2, 2]
    with pytest.raises(ValueError):
        range_minimums([1, 2], [(1, 0)])
    # Exhaustive cross-check against min() on every possible range.
    import random
    random.seed(3)
    data = [random.randint(-100, 100) for _ in range(60)]
    qs = [(lo, hi) for lo in range(len(data)) for hi in range(lo, len(data))]
    expected = [min(data[lo : hi + 1]) for lo, hi in qs]
    assert range_minimums(data, qs) == expected

def test_p07_count_smaller_after():
    """Count Of Smaller Numbers After Self — Fenwick tree (BIT) (Hard)."""
    assert count_smaller_after([5, 2, 6, 1]) == [2, 1, 1, 0]
    assert count_smaller_after([]) == []
    assert count_smaller_after([1]) == [0]
    # Ascending: nothing smaller follows anything.
    assert count_smaller_after([1, 2, 3]) == [0, 0, 0]
    # Descending: everything after is smaller.
    assert count_smaller_after([3, 2, 1]) == [2, 1, 0]
    # Duplicates are not STRICTLY smaller.
    assert count_smaller_after([2, 2, 2]) == [0, 0, 0]
    assert count_smaller_after([2, 1, 2]) == [1, 0, 0]
    # Negatives.
    assert count_smaller_after([-1, -2, 0]) == [1, 0, 0]
    # Cross-check against the O(n^2) brute force.
    import random
    random.seed(9)
    data = [random.randint(-30, 30) for _ in range(120)]
    brute = [
        sum(1 for j in range(i + 1, len(data)) if data[j] < data[i])
        for i in range(len(data))
    ]
    assert count_smaller_after(data) == brute
    # Scale: 10**5 descending values would be ~5*10^9 for the brute force.
    big = list(range(20_000, 0, -1))
    got = count_smaller_after(big)
    assert got[0] == 19_999 and got[-1] == 0

def test_p08_implement_prefix_map():
    """Prefix-Sum Map: Sum Of Keys With A Prefix — Trie with aggregated values (Medium)."""
    ops = [("insert", "apple", 3), ("sum", "ap", 0), ("insert", "app", 2), ("sum", "ap", 0)]
    assert simulate_prefix_map(ops) == [3, 5]
    # An unknown prefix sums to zero.
    assert simulate_prefix_map([("insert", "a", 1), ("sum", "z", 0)]) == [0]
    # The empty prefix totals everything.
    ops = [("insert", "a", 1), ("insert", "b", 2), ("sum", "", 0)]
    assert simulate_prefix_map(ops) == [3]
    # THE trap: re-inserting must REPLACE, not accumulate.
    ops = [("insert", "apple", 3), ("insert", "apple", 2), ("sum", "ap", 0)]
    assert simulate_prefix_map(ops) == [2]
    ops = [("insert", "a", 5), ("insert", "a", 1), ("sum", "a", 0), ("sum", "", 0)]
    assert simulate_prefix_map(ops) == [1, 1]
    # A key is its own prefix.
    assert simulate_prefix_map([("insert", "abc", 7), ("sum", "abc", 0)]) == [7]
    # A prefix longer than any key.
    assert simulate_prefix_map([("insert", "ab", 7), ("sum", "abc", 0)]) == [0]
    with pytest.raises(ValueError):
        simulate_prefix_map([("frobnicate", "x", 0)])
    # Cross-check against a plain dict on a long sequence.
    import random
    random.seed(13)
    keys = [''.join(random.choice('ab') for _ in range(random.randint(1, 4))) for _ in range(30)]
    seq, model, expected = [], {}, []
    for _ in range(500):
        if random.random() < 0.5:
            k, v = random.choice(keys), random.randint(-20, 20)
            seq.append(('insert', k, v))
            model[k] = v
        else:
            p = random.choice(['', *keys])
            seq.append(('sum', p, 0))
            expected.append(sum(v for k, v in model.items() if k.startswith(p)))
    assert simulate_prefix_map(seq) == expected
