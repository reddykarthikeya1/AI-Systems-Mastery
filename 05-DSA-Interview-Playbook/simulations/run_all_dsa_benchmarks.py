#!/usr/bin/env python3
"""
===============================================================================
DSA Core Patterns Test Runner & Verification Suite
===============================================================================
Executes automated unit test assertions and measures execution latency
across all primary algorithmic patterns featured in the DSA Playbook.
===============================================================================
"""

import time
import math
from collections import deque
from typing import List, Dict, Optional


# -------------------------------------------------------------------------
# 1. Pattern: Two Pointers (Convergence)
# -------------------------------------------------------------------------
def trap_rain_water(height: List[int]) -> int:
    if not height:
        return 0
    left, right = 0, len(height) - 1
    max_left, max_right = 0, 0
    water = 0

    while left < right:
        if height[left] < height[right]:
            if height[left] >= max_left:
                max_left = height[left]
            else:
                water += max_left - height[left]
            left += 1
        else:
            if height[right] >= max_right:
                max_right = height[right]
            else:
                water += max_right - height[right]
            right -= 1
    return water


# -------------------------------------------------------------------------
# 2. Pattern: Sliding Window (Dynamic Expansion & Contraction)
# -------------------------------------------------------------------------
def length_of_longest_substring(s: str) -> int:
    last_seen = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len


# -------------------------------------------------------------------------
# 3. Pattern: Monotonic Deque (Sliding Window Maximum)
# -------------------------------------------------------------------------
def max_sliding_window(nums: List[int], k: int) -> List[int]:
    if not nums or k == 0:
        return []
    dq = deque()
    result = []
    for i in range(len(nums)):
        if dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result


# -------------------------------------------------------------------------
# 4. Pattern: Fast & Slow Pointers (Cycle Detection)
# -------------------------------------------------------------------------
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def has_cycle(head: Optional[ListNode]) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


# -------------------------------------------------------------------------
# 5. Pattern: Trie with Wildcard Search
# -------------------------------------------------------------------------
class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_terminal: bool = False

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word: str) -> None:
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_terminal = True

    def search(self, word: str) -> bool:
        def dfs(node: TrieNode, idx: int) -> bool:
            if idx == len(word):
                return node.is_terminal
            char = word[idx]
            if char != ".":
                if char not in node.children:
                    return False
                return dfs(node.children[char], idx + 1)
            else:
                for child in node.children.values():
                    if dfs(child, idx + 1):
                        return True
                return False
        return dfs(self.root, 0)


# -------------------------------------------------------------------------
# 6. Pattern: Topological Sort (Kahn's BFS)
# -------------------------------------------------------------------------
def can_finish_courses(num_courses: int, prerequisites: List[List[int]]) -> bool:
    adj = {i: [] for i in range(num_courses)}
    in_degrees = [0] * num_courses
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degrees[course] += 1

    queue = deque([i for i in range(num_courses) if in_degrees[i] == 0])
    taken = 0
    while queue:
        curr = queue.popleft()
        taken += 1
        for nxt in adj[curr]:
            in_degrees[nxt] -= 1
            if in_degrees[nxt] == 0:
                queue.append(nxt)
    return taken == num_courses


# -------------------------------------------------------------------------
# 7. Pattern: Binary Search on Answer Space
# -------------------------------------------------------------------------
def min_eating_speed(piles: List[int], h: int) -> int:
    """Koko Eating Bananas: finds minimum integer k to eat all piles within h hours."""
    low, high = 1, max(piles)
    ans = high
    while low <= high:
        mid = (low + high) // 2
        total_hours = sum(math.ceil(p / mid) for p in piles)
        if total_hours <= h:
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
    return ans


# -------------------------------------------------------------------------
# Main Benchmark Runner
# -------------------------------------------------------------------------
def run_all_benchmarks():
    print("=" * 75)
    print(" DSA PLAYBOOK AUTOMATED VERIFICATION & BENCHMARK SUITE")
    print("=" * 75)

    tests = [
        ("Two Pointers (Trapping Rain Water)", lambda: trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6),
        ("Sliding Window (Longest Substring)", lambda: length_of_longest_substring("abcabcbb") == 3),
        ("Monotonic Deque (Window Maximum)", lambda: max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]),
        ("Fast & Slow Pointers (Cycle Detection)", lambda: has_cycle(ListNode(1, ListNode(2))) is False),
        ("Trie with Wildcard Search", lambda: (lambda wd: (wd.add_word("bad"), wd.add_word("dad"), wd.search(".ad"))[-1])(WordDictionary()) is True),
        ("Graph Topological Sort (Kahn's)", lambda: can_finish_courses(2, [[1, 0]]) is True and can_finish_courses(2, [[1, 0], [0, 1]]) is False),
        ("Binary Search on Answer (Koko Bananas)", lambda: min_eating_speed([3, 6, 7, 11], 8) == 4)
    ]

    print(f"{'Test Name':<42} | {'Status':<10} | {'Latency':<12}")
    print("-" * 75)

    all_passed = True
    for name, test_fn in tests:
        start_t = time.perf_counter()
        passed = test_fn()
        elapsed_us = (time.perf_counter() - start_t) * 1_000_000

        status_str = "PASS [OK]" if passed else "FAIL [XX]"
        if not passed:
            all_passed = False

        print(f"{name:<42} | {status_str:<10} | {elapsed_us:>8.2f} us")

    print("-" * 75)
    assert all_passed, "[FAIL] One or more DSA pattern tests failed!"
    print("[ALL PASS] All core DSA algorithmic patterns verified successfully.")
    print("=" * 75)


if __name__ == "__main__":
    run_all_benchmarks()
