"""
Problem 6: Product of Array Except Self (Medium - Arrays & Hashing)
Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`. Must run in $O(N)$ time without using division.
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

def product_except_self(nums: list[int]) -> list[int]:
    """Computes product of array except self without division.
    
    Time: O(N), Space: O(1) auxiliary (output array excluded)
    """
    raise NotImplementedError

