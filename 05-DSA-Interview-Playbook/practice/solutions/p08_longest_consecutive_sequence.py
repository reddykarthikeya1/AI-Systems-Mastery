"""
Problem 8: Longest Consecutive Sequence (Medium - Arrays & Hashing)
Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence. Must run in $O(N)$ time.
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

def longest_consecutive(nums: list[int]) -> int:
    """Finds length of longest consecutive sequence in O(N) time."""
    num_set = set(nums)
    longest = 0
    
    for num in num_set:
        # Check if num is the start of a sequence
        if (num - 1) not in num_set:
            current_num = num
            current_streak = 1
            while (current_num + 1) in num_set:
                current_num += 1
                current_streak += 1
            longest = max(longest, current_streak)
            
    return longest


def run_tests():
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive([]) == 0
    assert longest_consecutive([1, 2, 0, 1]) == 3
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p08_longest_consecutive_sequence!")
