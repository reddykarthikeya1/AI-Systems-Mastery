"""
Problem 16: Minimum Window Substring (Hard - Sliding Window)
Given two strings `s` and `t` of lengths $m$ and $n$ respectively, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If no such substring exists, return empty string `""`.
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

def min_window(s: str, t: str) -> str:
    """Finds minimum window substring of s containing all characters of t.
    
    Time: O(M + N), Space: O(M + N)
    """
    if not s or not t:
        return ""
        
    need: dict[str, int] = {}
    for c in t:
        need[c] = need.get(c, 0) + 1
        
    have: dict[str, int] = {}
    matched = 0
    left = 0
    min_len = float("inf")
    res_indices = (-1, -1)
    
    for right in range(len(s)):
        char = s[right]
        have[char] = have.get(char, 0) + 1
        
        if char in need and have[char] == need[char]:
            matched += 1
            
        while matched == len(need):
            if (right - left + 1) < min_len:
                min_len = right - left + 1
                res_indices = (left, right)
                
            left_char = s[left]
            have[left_char] -= 1
            if left_char in need and have[left_char] < need[left_char]:
                matched -= 1
            left += 1
            
    l, r = res_indices
    return s[l : r + 1] if min_len != float("inf") else ""


def run_tests():
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "a") == "a"
    assert min_window("a", "aa") == ""
    assert min_window("ab", "b") == "b"
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p16_minimum_window_substring!")
