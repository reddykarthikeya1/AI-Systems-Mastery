"""
Problem 23: Reverse Linked List (Easy - Linked List)
Given the `head` of a singly linked list, reverse the list, and return the reversed list.
"""
from typing import List, Dict, Optional, Tuple, Set
import heapq
from collections import deque, defaultdict
import bisect

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def from_list(vals):
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverses singly linked list in-place in O(N) time, O(1) space."""
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev


def run_tests():
    # Helper to build and read
    def to_list(head):
        res = []
        while head:
            res.append(head.val)
            head = head.next
        return res
    
    def from_list(vals):
        dummy = ListNode(0)
        curr = dummy
        for v in vals:
            curr.next = ListNode(v)
            curr = curr.next
        return dummy.next
    
    assert to_list(reverse_list(from_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
    assert to_list(reverse_list(from_list([1, 2]))) == [2, 1]
    assert to_list(reverse_list(from_list([]))) == []
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p23_reverse_linked_list!")
