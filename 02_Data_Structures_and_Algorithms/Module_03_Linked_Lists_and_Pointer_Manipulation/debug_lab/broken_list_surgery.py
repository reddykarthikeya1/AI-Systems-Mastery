#!/usr/bin/env python3
"""Linked-list utilities. Exits 0, and loses your data politely.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

RULE = "=" * 68


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val: int = 0, nxt: "ListNode | None" = None) -> None:
        self.val = val
        self.next = nxt


def from_list(values: list[int]) -> "ListNode | None":
    head: ListNode | None = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head: "ListNode | None", limit: int = 50) -> list[int]:
    out: list[int] = []
    node = head
    while node is not None:
        out.append(node.val)
        if len(out) > limit:
            out.append(-999)        # cycle guard
            break
        node = node.next
    return out


def build_cycle(values: list[int], pos: int) -> "ListNode | None":
    if not values:
        return None
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0]


def reverse_list(head: "ListNode | None") -> "ListNode | None":
    prev: ListNode | None = None
    cur = head
    while cur is not None:
        cur.next = prev
        prev = cur
        cur = cur.next
    return prev


def has_cycle(head: "ListNode | None") -> bool:
    seen_positions = 0
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next
        seen_positions += 1
        if slow is fast:
            return True
        if seen_positions > 10_000:
            return False
    return False


def middle_node(head: "ListNode | None") -> "ListNode | None":
    slow = fast = head
    while fast is not None and fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow


def merge_sorted(a: "ListNode | None", b: "ListNode | None") -> "ListNode | None":
    dummy = ListNode(0)
    tail = dummy
    while a is not None and b is not None:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    return dummy.next


def main() -> None:
    print(RULE)
    print("LINKED LIST UTILITIES")
    print(RULE)

    print()
    print("[1] Reversal")
    for values in ([1, 2, 3], [1, 2], [1], [1, 2, 3, 4, 5]):
        got = to_list(reverse_list(from_list(values)))
        print(f"      {values} -> {got}   (expected {values[::-1]})")

    print()
    print("[2] Cycle detection")
    cases = [([3, 2, 0, -4], 1, True), ([1, 2], 0, True), ([1], 0, True),
             ([1, 2], -1, False), ([1, 2, 3], -1, False)]
    for values, pos, expected in cases:
        got = has_cycle(build_cycle(values, pos))
        print(f"      {values} cycle_at={pos:<3} -> {got}   (expected {expected})")

    print()
    print("[3] Middle node")
    for values, expected in (([1, 2, 3, 4, 5], 3), ([1, 2, 3, 4, 5, 6], 4),
                             ([1, 2], 2), ([1], 1)):
        node = middle_node(from_list(values))
        got = node.val if node else None
        print(f"      {values} -> {got}   (expected {expected})")

    print()
    print("[4] Merging two sorted lists")
    for xs, ys in (([1, 2, 4], [1, 3, 4]), ([1, 2, 3], [4, 5]), ([], [1, 2]),
                   ([5], [1, 2, 3])):
        got = to_list(merge_sorted(from_list(xs), from_list(ys)))
        print(f"      {xs} + {ys} -> {got}   (expected {sorted(xs + ys)})")

    print()
    print(RULE)
    print("Utilities check complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
