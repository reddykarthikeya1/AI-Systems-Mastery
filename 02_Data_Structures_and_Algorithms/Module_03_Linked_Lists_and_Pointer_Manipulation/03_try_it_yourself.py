"""Module 03: Interactive Linked List CLI Sandbox."""
from __future__ import annotations


class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None):
        self.val = val
        self.next = next


def print_list(head: ListNode | None) -> str:
    vals = []
    curr = head
    while curr:
        vals.append(str(curr.val))
        curr = curr.next
    return " -> ".join(vals) if vals else "Empty"


def demo():
    print("\n=== DEMO: In-Place Linked List Reversal ===")
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))
    print("Original List:", print_list(head))

    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    print("Reversed List:", print_list(prev))


if __name__ == "__main__":
    demo()
