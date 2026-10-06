"""
Problem 6: Product of Array Except Self (Medium - Arrays & Hashing)
Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`. Must run in $O(N)$ time without using division.
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

def product_except_self(nums: list[int]) -> list[int]:
    """Computes product of array except self without division.
    
    Time: O(N), Space: O(1) auxiliary (output array excluded)
    """
    n = len(nums)
    res = [1] * n
    
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
        
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
        
    return res


def run_tests():
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    assert product_except_self([2, 3]) == [3, 2]
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p06_product_except_self!")
