"""
Problem 28: Merge K Sorted Lists (Hard - Linked List)
You are given an array of $k$ linked-lists `lists`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.
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

import heapq

def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    """Merges k sorted linked lists using a min-heap in O(N log k) time."""
    dummy = ListNode(0)
    curr = dummy
    heap: list[tuple[int, int, ListNode]] = []
    
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
            
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
            
    return dummy.next


def run_tests():
    l1 = from_list([1, 4, 5])
    l2 = from_list([1, 3, 4])
    l3 = from_list([2, 6])
    assert to_list(merge_k_lists([l1, l2, l3])) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert to_list(merge_k_lists([])) == []
    assert to_list(merge_k_lists([None])) == []
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p28_merge_k_sorted_lists!")
