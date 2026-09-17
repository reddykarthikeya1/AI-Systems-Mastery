"""Beginner playground for Module 03 - Linked Lists & Pointer Manipulation.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

# -------------------------------------------- 1. Node Definition and Pointer Traversal
@dataclass
class Node:
    val: int
    next: Optional['Node'] = None

head = Node(1, Node(2, Node(3)))
vals = []
curr = head
while curr:
    vals.append(curr.val)
    curr = curr.next

assert vals == [1, 2, 3]
assert head.next.val == 2
print(f"Traversed linked list: {vals}")

# -------------------------------------------- 2. Three-Pointer In-Place Reversal
prev = None
curr = head
while curr:
    nxt = curr.next
    curr.next = prev
    prev = curr
    curr = nxt

new_head = prev
reversed_vals = []
curr = new_head
while curr:
    reversed_vals.append(curr.val)
    curr = curr.next

assert reversed_vals == [3, 2, 1]
assert new_head.val == 3
print(f"Reversed list: {reversed_vals}")

# -------------------------------------------- 3. Floyd's Tortoise and Hare Cycle Invariant
n1, n2, n3 = Node(10), Node(20), Node(30)
n1.next = n2
n2.next = n3
n3.next = n2  # cycle back to n2

slow, fast = n1, n1
has_cycle = False
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        has_cycle = True
        break

assert has_cycle is True, "Cycle must be detected"
assert slow.val == 20 or slow.val == 30
print(f"Cycle detected successfully inside loop at node with val={slow.val}")

print()
print("All checks passed.")
