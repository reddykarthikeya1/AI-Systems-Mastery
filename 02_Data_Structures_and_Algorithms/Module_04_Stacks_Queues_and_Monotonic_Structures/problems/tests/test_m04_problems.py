"""Problem-bank suite for Module_04_Stacks_Queues_and_Monotonic_Structures.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

import pytest
from p01_balanced_brackets import balanced_brackets
from p02_next_greater import next_greater
from p03_daily_temperatures import daily_temperatures
from p04_largest_rectangle import largest_rectangle
from p05_sliding_window_max import sliding_window_max
from p06_min_stack import simulate_min_stack
from p07_eval_rpn import eval_rpn
from p08_decode_string import decode_string


def test_p01_balanced_brackets():
    """Valid Parentheses — Stack (Easy)."""
    assert balanced_brackets("()") is True
    assert balanced_brackets("()[]{}") is True
    assert balanced_brackets("{[()]}") is True
    # Correct counts, wrong nesting order.
    assert balanced_brackets("([)]") is False
    assert balanced_brackets("(]") is False
    # Unclosed opener - the "stack not empty at the end" case.
    assert balanced_brackets("(") is False
    assert balanced_brackets("([]") is False
    # Closer with nothing open.
    assert balanced_brackets(")") is False
    assert balanced_brackets("()]") is False
    assert balanced_brackets("") is True

def test_p02_next_greater():
    """Next Greater Element — Monotonic stack (Medium)."""
    assert next_greater([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]
    assert next_greater([1, 2, 3]) == [2, 3, -1]
    assert next_greater([3, 2, 1]) == [-1, -1, -1]
    assert next_greater([]) == []
    assert next_greater([5]) == [-1]
    # Equal values: 'strictly greater' means a duplicate does not count.
    assert next_greater([2, 2, 2]) == [-1, -1, -1]
    assert next_greater([1, 1, 2]) == [2, 2, -1]
    assert next_greater([-1, -3, -2]) == [-1, -2, -1]
    # Cross-check against brute force.
    data = [4, 1, 7, 3, 3, 9, 2, 8, 8, 1]
    brute = [
        next((data[j] for j in range(i + 1, len(data)) if data[j] > data[i]), -1)
        for i in range(len(data))
    ]
    assert next_greater(data) == brute
    # O(n): a quadratic solution would be ~10^10 operations here.
    big = list(range(100_000, 0, -1))
    assert next_greater(big) == [-1] * 100_000

def test_p03_daily_temperatures():
    """Daily Temperatures — Monotonic stack (Medium)."""
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert daily_temperatures([30, 60, 90]) == [1, 1, 0]
    assert daily_temperatures([90, 60, 30]) == [0, 0, 0]
    assert daily_temperatures([50]) == [0]
    # Equal temperatures are not warmer.
    assert daily_temperatures([50, 50, 50]) == [0, 0, 0]
    assert daily_temperatures([50, 50, 51]) == [2, 1, 0]
    # Cross-check.
    data = [55, 38, 53, 81, 61, 93, 97, 32, 43, 78]
    brute = [
        next((j - i for j in range(i + 1, len(data)) if data[j] > data[i]), 0)
        for i in range(len(data))
    ]
    assert daily_temperatures(data) == brute

def test_p04_largest_rectangle():
    """Largest Rectangle In A Histogram — Monotonic stack (Hard)."""
    assert largest_rectangle([2, 1, 5, 6, 2, 3]) == 10
    assert largest_rectangle([2, 4]) == 4
    assert largest_rectangle([]) == 0
    assert largest_rectangle([5]) == 5
    # Uniform heights: the whole histogram.
    assert largest_rectangle([3, 3, 3]) == 9
    # Zeros split the histogram.
    assert largest_rectangle([0, 0, 0]) == 0
    assert largest_rectangle([2, 0, 2]) == 2
    # Monotonic in both directions.
    assert largest_rectangle([1, 2, 3, 4, 5]) == 9
    assert largest_rectangle([5, 4, 3, 2, 1]) == 9
    # Cross-check against an O(n^2) brute force.
    data = [6, 2, 5, 4, 5, 1, 6]
    brute = max(
        min(data[i : j + 1]) * (j - i + 1)
        for i in range(len(data))
        for j in range(i, len(data))
    )
    assert largest_rectangle(data) == brute
    # O(n) required.
    assert largest_rectangle([1] * 100_000) == 100_000

def test_p05_sliding_window_max():
    """Sliding Window Maximum — Monotonic deque (Hard)."""
    assert sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert sliding_window_max([1], 1) == [1]
    assert sliding_window_max([1, -1], 1) == [1, -1]
    # Window equal to the whole array.
    assert sliding_window_max([9, 11], 2) == [11]
    assert sliding_window_max([4, -2], 2) == [4]
    # Duplicates must not break the domination rule.
    assert sliding_window_max([2, 2, 2], 2) == [2, 2]
    # Monotonic inputs exercise both eviction paths.
    assert sliding_window_max([1, 2, 3, 4, 5], 2) == [2, 3, 4, 5]
    assert sliding_window_max([5, 4, 3, 2, 1], 2) == [5, 4, 3, 2]
    with pytest.raises(ValueError):
        sliding_window_max([1, 2, 3], 0)
    with pytest.raises(ValueError):
        sliding_window_max([1, 2, 3], 4)
    # Cross-check against the naive per-window max.
    data = [8, 3, -1, 7, 7, 2, 9, 0, 4, 4, 1]
    for k in range(1, len(data) + 1):
        brute = [max(data[i : i + k]) for i in range(len(data) - k + 1)]
        assert sliding_window_max(data, k) == brute, k
    # O(n) required.
    big = list(range(100_000))
    assert sliding_window_max(big, 3)[-1] == 99_999

def test_p06_min_stack():
    """Min Stack (O(1) Minimum) — Stack with auxiliary state (Medium)."""
    ops = [("push", 3), ("push", 1), ("get_min", None), ("pop", None), ("get_min", None)]
    assert simulate_min_stack(ops) == [1, 3]
    ops = [("push", -2), ("push", 0), ("push", -3), ("get_min", None),
           ("pop", None), ("top", None), ("get_min", None)]
    assert simulate_min_stack(ops) == [-3, 0, -2]
    # Empty stack must yield None, not raise.
    assert simulate_min_stack([("top", None), ("get_min", None)]) == [None, None]
    assert simulate_min_stack([("pop", None), ("get_min", None)]) == [None]
    # Duplicate minima: popping one must not lose the other.
    ops = [("push", 2), ("push", 2), ("get_min", None), ("pop", None), ("get_min", None)]
    assert simulate_min_stack(ops) == [2, 2]
    # A rising sequence never changes the minimum.
    ops = [("push", 1), ("push", 2), ("push", 3), ("get_min", None)]
    assert simulate_min_stack(ops) == [1]
    with pytest.raises(ValueError):
        simulate_min_stack([("frobnicate", None)])
    # Cross-check against a naive model on a long op sequence.
    import random
    random.seed(7)
    seq, model, expected = [], [], []
    for _ in range(2000):
        r = random.random()
        if r < 0.5:
            v = random.randint(-50, 50)
            seq.append(('push', v))
            model.append(v)
        elif r < 0.7:
            seq.append(('pop', None))
            if model: model.pop()
        elif r < 0.85:
            seq.append(('top', None))
            expected.append(model[-1] if model else None)
        else:
            seq.append(('get_min', None))
            expected.append(min(model) if model else None)
    assert simulate_min_stack(seq) == expected

def test_p07_eval_rpn():
    """Evaluate Reverse Polish Notation — Stack (Medium)."""
    assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
    assert eval_rpn(["4", "13", "5", "/", "+"]) == 6
    assert eval_rpn(["5"]) == 5
    assert eval_rpn(["-5"]) == -5
    # Operand order for the non-commutative operators.
    assert eval_rpn(["7", "2", "-"]) == 5
    assert eval_rpn(["7", "2", "/"]) == 3
    # Truncation toward zero, NOT floor. Python // would give -4.
    assert eval_rpn(["-7", "2", "/"]) == -3
    assert eval_rpn(["7", "-2", "/"]) == -3
    assert eval_rpn(["-7", "-2", "/"]) == 3
    # A longer expression.
    assert eval_rpn(["10","6","9","3","+","-11","*","/","*","17","+","5","+"]) == 22
    # Malformed inputs must raise.
    with pytest.raises(ValueError):
        eval_rpn(["+"])
    with pytest.raises(ValueError):
        eval_rpn(["1", "2"])
    with pytest.raises(ValueError):
        eval_rpn(["1", "0", "/"])
    with pytest.raises(ValueError):
        eval_rpn(["1", "x", "+"])

def test_p08_decode_string():
    """Decode String — Stack of contexts (Medium)."""
    assert decode_string("3[a]2[bc]") == "aaabcbc"
    assert decode_string("3[a2[c]]") == "accaccacc"
    assert decode_string("2[abc]3[cd]ef") == "abcabccdcdcdef"
    assert decode_string("abc") == "abc"
    assert decode_string("1[a]") == "a"
    # Multi-digit repeat counts.
    assert decode_string("10[a]") == "a" * 10
    assert decode_string("12[ab]") == "ab" * 12
    # Deep nesting.
    assert decode_string("2[2[2[a]]]") == "a" * 8
    # Text before, inside and after a group.
    assert decode_string("x2[y3[z]]w") == "xyzzzyzzzw"
    with pytest.raises(ValueError):
        decode_string("2[a")
    with pytest.raises(ValueError):
        decode_string("2[a]]")
