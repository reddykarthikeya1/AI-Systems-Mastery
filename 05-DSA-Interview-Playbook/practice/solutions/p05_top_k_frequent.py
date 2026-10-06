"""
Problem 5: Top K Frequent Elements (Medium - Arrays & Hashing)
Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.
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

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """Returns the k most frequent elements using bucket sort.
    
    Time: O(N), Space: O(N)
    """
    counts: dict[int, int] = {}
    for num in nums:
        counts[num] = counts.get(num, 0) + 1
    
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for val, freq in counts.items():
        buckets[freq].append(val)
    
    res: list[int] = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            res.append(num)
            if len(res) == k:
                return res
    return res


def run_tests():
    assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    assert top_k_frequent([1], 1) == [1]
    assert sorted(top_k_frequent([4, 1, -1, 2, -1, 2, 3], 2)) == [-1, 2]
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p05_top_k_frequent!")
