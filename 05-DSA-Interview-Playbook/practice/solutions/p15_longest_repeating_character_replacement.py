"""
Problem 15: Longest Repeating Character Replacement (Medium - Sliding Window)
You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character at most `k` times. Return the length of the longest substring containing the same letter you can get after performing above operations.
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

def character_replacement(s: str, k: int) -> int:
    """Finds longest repeating character substring after at most k replacements.
    
    Time: O(N), Space: O(1)
    """
    counts: dict[str, int] = {}
    left = 0
    max_freq = 0
    max_len = 0
    
    for right in range(len(s)):
        ch = s[right]
        counts[ch] = counts.get(ch, 0) + 1
        max_freq = max(max_freq, counts[ch])
        
        while (right - left + 1) - max_freq > k:
            counts[s[left]] -= 1
            left += 1
            
        max_len = max(max_len, right - left + 1)
        
    return max_len


def run_tests():
    assert character_replacement("ABAB", 2) == 4
    assert character_replacement("AABABBA", 1) == 4
    assert character_replacement("AAAA", 2) == 4
    assert character_replacement("ABBB", 2) == 4
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p15_longest_repeating_character_replacement!")
