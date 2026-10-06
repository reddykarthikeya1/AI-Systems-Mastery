"""
Problem 25: Reorder List (Medium - Linked List)
You are given the head of a singly linked-list: $L_0 \to L_1 \to \dots \to L_{n - 1} \to L_n$. Reorder the list to: $L_0 \to L_n \to L_1 \to L_{n - 1} \to L_2 \to L_{n - 2} \dots$ in-place without modifying node values.
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

def reorder_list(head: Optional[ListNode]) -> None:
    """Reorders list in-place to L0 -> Ln -> L1 -> Ln-1 ..."""
    if not head or not head.next:
        return
        
    # 1. Find middle node
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
    # 2. Reverse second half
    second = slow.next
    slow.next = None
    prev = None
    while second:
        nxt = second.next
        second.next = prev
        prev = second
        second = nxt
        
    # 3. Interleave two halves
    first, second = head, prev
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2


def run_tests():
    h1 = from_list([1, 2, 3, 4])
    reorder_list(h1)
    assert to_list(h1) == [1, 4, 2, 3]
    
    h2 = from_list([1, 2, 3, 4, 5])
    reorder_list(h2)
    assert to_list(h2) == [1, 5, 2, 4, 3]
    
    h3 = from_list([1])
    reorder_list(h3)
    assert to_list(h3) == [1]
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p25_reorder_list!")
