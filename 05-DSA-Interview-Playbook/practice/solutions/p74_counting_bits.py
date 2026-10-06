"""
Problem 74: Counting Bits (Easy - Bit Manipulation)
Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` ($0 \le i \le n$), `ans[i]` is the number of 1's in the binary representation of `i`. Must run in $O(N)$ linear time.
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

def count_bits(n: int) -> list[int]:
    """Counts set bits for all integers 0 to n in linear O(N) time."""
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp


def run_tests():
    assert count_bits(2) == [0, 1, 1]
    assert count_bits(5) == [0, 1, 1, 2, 1, 2]
    assert count_bits(0) == [0]
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p74_counting_bits!")
