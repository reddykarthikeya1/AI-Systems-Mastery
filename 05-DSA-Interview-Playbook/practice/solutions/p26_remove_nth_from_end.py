"""
Problem 26: Remove Nth Node From End of List (Medium - Linked List)
Given the `head` of a linked list, remove the $n^{\text{th}}$ node from the end of the list and return its head in one single pass.
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

def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """Removes nth node from end of list in a single pass."""
    dummy = ListNode(0, head)
    slow = dummy
    fast = head
    
    # Advance fast by n steps
    for _ in range(n):
        if fast:
            fast = fast.next
            
    while fast:
        slow = slow.next
        fast = fast.next
        
    slow.next = slow.next.next
    return dummy.next


def run_tests():
    assert to_list(remove_nth_from_end(from_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
    assert to_list(remove_nth_from_end(from_list([1]), 1)) == []
    assert to_list(remove_nth_from_end(from_list([1, 2]), 1)) == [1]
    assert to_list(remove_nth_from_end(from_list([1, 2]), 2)) == [2]
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p26_remove_nth_from_end!")
