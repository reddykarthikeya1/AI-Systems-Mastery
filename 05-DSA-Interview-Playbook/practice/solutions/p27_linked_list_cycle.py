"""
Problem 27: Linked List Cycle (Easy - Linked List)
Given `head`, the head of a linked list, determine if the linked list has a cycle in it using $O(1)$ memory.
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

def has_cycle(head: Optional[ListNode]) -> bool:
    """Detects cycle using Floyd's Tortoise and Hare algorithm in O(1) space."""
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
            
    return False


def run_tests():
    n1, n2, n3, n4 = ListNode(3), ListNode(2), ListNode(0), ListNode(-4)
    n1.next, n2.next, n3.next, n4.next = n2, n3, n4, n2
    assert has_cycle(n1) is True
    
    n_no_cycle = from_list([1, 2, 3])
    assert has_cycle(n_no_cycle) is False
    assert has_cycle(None) is False
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p27_linked_list_cycle!")
