"""
Problem 42: Kth Largest Element in an Array (Medium - Heap / Priority Queue)
Given an integer array `nums` and an integer `k`, return the $k^{\text{th}}$ largest element in the array. Note that it is the $k^{\text{th}}$ largest element in sorted order, not the $k^{\text{th}}$ distinct element.
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

def find_kth_largest(nums: list[int], k: int) -> int:
    """Finds kth largest element using min-heap in O(N log k) time."""
    heap: list[int] = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


def run_tests():
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert find_kth_largest([1], 1) == 1
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p42_kth_largest_element_in_an_array!")
