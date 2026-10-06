"""
Problem 62: Decode Ways (Medium - Dynamic Programming)
A message containing letters from A-Z can be encoded into numbers using the mapping `'A' -> 1, 'B' -> 2, ... 'Z' -> 26`. Given a string `s` containing only digits, return the number of ways to decode it.
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

def num_decodings(s: str) -> int:
    """Calculates number of ways to decode string of digits in O(N) time."""
    if not s or s[0] == "0":
        return 0
        
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    
    for i in range(2, n + 1):
        # One digit check
        if s[i - 1] != "0":
            dp[i] += dp[i - 1]
            
        # Two digit check
        two_digit = int(s[i - 2 : i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i - 2]
            
    return dp[n]


def run_tests():
    assert num_decodings("12") == 2
    assert num_decodings("226") == 3
    assert num_decodings("06") == 0 # Leading zero cannot be decoded
    assert num_decodings("10") == 1
    assert num_decodings("27") == 1
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p62_decode_ways!")
