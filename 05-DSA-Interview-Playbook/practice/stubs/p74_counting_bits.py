"""
Problem 74: Counting Bits (Easy - Bit Manipulation)
Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` ($0 \le i \le n$), `ans[i]` is the number of 1's in the binary representation of `i`. Must run in $O(N)$ linear time.
"""
from typing import List, Dict, Optional, Tuple, Set

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

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
    raise NotImplementedError

