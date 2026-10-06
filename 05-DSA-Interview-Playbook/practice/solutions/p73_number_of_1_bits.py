"""
Problem 73: Number of 1 Bits (Easy - Bit Manipulation)
Given a positive integer `n`, write a function that returns the number of set bits (1s) it has (also known as the Hamming weight).
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

def hamming_weight(n: int) -> int:
    """Counts set bits in integer using Brian Kernighan's algorithm."""
    count = 0
    while n:
        n &= (n - 1)
        count += 1
    return count


def run_tests():
    assert hamming_weight(11) == 3 # 1011
    assert hamming_weight(128) == 1 # 10000000
    assert hamming_weight(2147483645) == 30
    assert hamming_weight(0) == 0
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p73_number_of_1_bits!")
