"""Problem-bank suite for Module_03_Linked_Lists_and_Pointer_Manipulation.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

from linked_list_common import build_cycle, from_list, node_at, to_list
from p01_reverse_list import reverse_list
from p02_has_cycle import has_cycle
from p03_cycle_start import cycle_start
from p04_middle_node import middle_node
from p05_merge_sorted import merge_sorted
from p06_remove_nth_from_end import remove_nth_from_end
from p07_is_palindrome_list import is_palindrome_list
from p08_reorder_list import reorder_list


def test_p01_reverse_list():
    """Reverse A Linked List — Pointer manipulation (Easy)."""
    assert to_list(reverse_list(from_list([1, 2, 3]))) == [3, 2, 1]
    assert to_list(reverse_list(from_list([1]))) == [1]
    assert reverse_list(None) is None
    assert to_list(reverse_list(from_list([1, 2]))) == [2, 1]
    # Reversing twice must return the original order.
    assert to_list(reverse_list(reverse_list(from_list([1, 2, 3, 4, 5])))) == [1, 2, 3, 4, 5]
    # Long list: a recursive solution would hit Python's 1000-frame limit.
    big = list(range(5000))
    assert to_list(reverse_list(from_list(big))) == big[::-1]

def test_p02_has_cycle():
    """Detect A Cycle — Fast and slow pointers (Easy)."""
    assert has_cycle(build_cycle([3, 2, 0, -4], 1)) is True
    assert has_cycle(build_cycle([1, 2], 0)) is True
    # A single node pointing at itself.
    assert has_cycle(build_cycle([1], 0)) is True
    assert has_cycle(build_cycle([1, 2], -1)) is False
    assert has_cycle(build_cycle([1], -1)) is False
    assert has_cycle(None) is False
    # Must not raise on short acyclic lists - the classic None-deref bug.
    assert has_cycle(from_list([1])) is False
    assert has_cycle(from_list([1, 2, 3])) is False

def test_p03_cycle_start():
    """Find Where The Cycle Begins — Floyd's algorithm (Medium)."""
    head = build_cycle([3, 2, 0, -4], 1)
    start = cycle_start(head)
    assert start is not None and start.val == 2
    assert start is node_at(head, 1)
    # Cycle back to the head itself.
    h2 = build_cycle([1, 2, 3], 0)
    assert cycle_start(h2) is h2
    # Self-loop on a single node.
    h3 = build_cycle([7], 0)
    assert cycle_start(h3) is h3
    # No cycle.
    assert cycle_start(build_cycle([1, 2], -1)) is None
    assert cycle_start(from_list([1, 2, 3])) is None
    assert cycle_start(None) is None
    assert cycle_start(from_list([1])) is None

def test_p04_middle_node():
    """Middle Of The List — Fast and slow pointers (Easy)."""
    m = middle_node(from_list([1, 2, 3, 4, 5]))
    assert m is not None and m.val == 3
    # Even length must give the SECOND middle.
    m = middle_node(from_list([1, 2, 3, 4, 5, 6]))
    assert m is not None and m.val == 4
    m = middle_node(from_list([1, 2]))
    assert m is not None and m.val == 2
    m = middle_node(from_list([1]))
    assert m is not None and m.val == 1
    assert middle_node(None) is None
    # The returned node must be the real node, not a copy - the rest of, # the list must still hang off it.
    head = from_list([1, 2, 3, 4, 5])
    assert to_list(middle_node(head)) == [3, 4, 5]

def test_p05_merge_sorted():
    """Merge Two Sorted Lists — Dummy head + two pointers (Easy)."""
    assert to_list(merge_sorted(from_list([1, 2, 4]), from_list([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]
    assert to_list(merge_sorted(from_list([]), from_list([0]))) == [0]
    assert merge_sorted(None, None) is None
    assert to_list(merge_sorted(from_list([1, 2]), None)) == [1, 2]
    assert to_list(merge_sorted(None, from_list([3, 4]))) == [3, 4]
    # Disjoint ranges, both directions.
    assert to_list(merge_sorted(from_list([1, 2, 3]), from_list([4, 5]))) == [1, 2, 3, 4, 5]
    assert to_list(merge_sorted(from_list([4, 5]), from_list([1, 2, 3]))) == [1, 2, 3, 4, 5]
    # All values equal.
    assert to_list(merge_sorted(from_list([2, 2]), from_list([2, 2]))) == [2, 2, 2, 2]
    # Nodes must be spliced, not copied: the result must contain the, # very node objects that were passed in.
    x, y = from_list([1]), from_list([2])
    merged = merge_sorted(x, y)
    assert merged is x and merged.next is y

def test_p06_remove_nth_from_end():
    """Remove The N-th Node From The End — Dummy head + gap pointers (Medium)."""
    assert to_list(remove_nth_from_end(from_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
    # Removing the only node.
    assert remove_nth_from_end(from_list([1]), 1) is None
    # Removing the head - the case the dummy node exists for.
    assert to_list(remove_nth_from_end(from_list([1, 2]), 2)) == [2]
    # Removing the tail.
    assert to_list(remove_nth_from_end(from_list([1, 2]), 1)) == [1]
    assert to_list(remove_nth_from_end(from_list([1, 2, 3]), 3)) == [2, 3]
    # Every position in a 5-list.
    for k in range(1, 6):
        expected = [1, 2, 3, 4, 5]
        del expected[len(expected) - k]
        assert to_list(remove_nth_from_end(from_list([1, 2, 3, 4, 5]), k)) == expected

def test_p07_is_palindrome_list():
    """Palindrome Linked List — Fast/slow + in-place reversal (Medium)."""
    assert is_palindrome_list(from_list([1, 2, 2, 1])) is True
    assert is_palindrome_list(from_list([1, 2])) is False
    # Odd length - the unpaired middle must be ignored.
    assert is_palindrome_list(from_list([1, 2, 1])) is True
    assert is_palindrome_list(from_list([1, 2, 3, 2, 1])) is True
    assert is_palindrome_list(from_list([1, 2, 3, 1])) is False
    assert is_palindrome_list(from_list([1])) is True
    assert is_palindrome_list(None) is True
    assert is_palindrome_list(from_list([1, 1])) is True
    # Long palindrome: must not recurse.
    half = list(range(50_000))
    assert is_palindrome_list(from_list(half + half[::-1])) is True

def test_p08_reorder_list():
    """Reorder List — Split + reverse + weave (Hard)."""
    assert to_list(reorder_list(from_list([1, 2, 3, 4]))) == [1, 4, 2, 3]
    assert to_list(reorder_list(from_list([1, 2, 3, 4, 5]))) == [1, 5, 2, 4, 3]
    assert to_list(reorder_list(from_list([1, 2]))) == [1, 2]
    assert to_list(reorder_list(from_list([1]))) == [1]
    assert reorder_list(None) is None
    assert to_list(reorder_list(from_list([1, 2, 3]))) == [1, 3, 2]
    # to_list raises on a cycle, so these also prove no cycle was created.
    for n in range(1, 12):
        vals = list(range(1, n + 1))
        got = to_list(reorder_list(from_list(vals)))
        assert sorted(got) == vals, n
        assert len(got) == n, n
    # Larger case, and it must terminate.
    got = to_list(reorder_list(from_list(list(range(10_000)))))
    assert len(got) == 10_000 and got[0] == 0 and got[1] == 9999
