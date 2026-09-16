"""Shared linked-list scaffolding for Module 03's problems.

This is plumbing, not an exercise - the problems are phrased in terms of it.
``from_list`` / ``to_list`` exist so the tests can state inputs and expected
outputs as plain Python lists, which keeps the assertions readable.
"""

from __future__ import annotations


class ListNode:
    __slots__ = ("next", "val")

    def __init__(self, val: int = 0, nxt: ListNode | None = None) -> None:
        self.val = val
        self.next = nxt

    def __repr__(self) -> str:
        return f"ListNode({self.val})"


def from_list(values: list[int]) -> ListNode | None:
    """Build a chain from a Python list. Returns the head, or None if empty."""
    head: ListNode | None = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head: ListNode | None, limit: int = 100_000) -> list[int]:
    """Flatten a chain back to a list.

    ``limit`` turns an accidental cycle into a fast failure instead of a hang -
    a pointer bug in your reversal should not lock up the test runner.
    """
    out: list[int] = []
    node = head
    while node is not None:
        out.append(node.val)
        if len(out) > limit:
            raise RuntimeError("cycle detected while flattening - check your pointers")
        node = node.next
    return out


def build_cycle(values: list[int], pos: int) -> ListNode | None:
    """Build a chain whose tail links back to index ``pos`` (-1 for no cycle)."""
    if not values:
        return None
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0]


def node_at(head: ListNode | None, index: int) -> ListNode | None:
    node = head
    for _ in range(index):
        if node is None:
            return None
        node = node.next
    return node
