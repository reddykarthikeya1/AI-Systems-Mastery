"""
Problem 4: Group Anagrams (Medium - Arrays & Hashing)
Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.
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

def group_anagrams(strs: list[str]) -> list[list[str]]:
    """Groups strings that are anagrams of each other.
    
    Time: O(N * K), Space: O(N * K)
    """
    groups: dict[tuple[int, ...], list[str]] = {}
    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1
        key = tuple(count)
        groups.setdefault(key, []).append(s)
    return list(groups.values())


def run_tests():
    res1 = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert sorted([sorted(g) for g in res1]) == sorted([["bat"], ["nat", "tan"], ["ate", "eat", "tea"]])
    assert group_anagrams([""]) == [[""]]
    assert group_anagrams(["a"]) == [["a"]]
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p04_group_anagrams!")
