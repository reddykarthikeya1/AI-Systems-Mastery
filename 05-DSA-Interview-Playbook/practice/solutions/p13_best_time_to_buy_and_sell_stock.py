"""
Problem 13: Best Time to Buy and Sell Stock (Easy - Sliding Window)
You are given an array `prices` where `prices[i]` is the price of a given stock on the $i^{\text{th}}$ day. Maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
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

def max_profit(prices: list[int]) -> int:
    """Calculates maximum profit from a single buy and sell transaction.
    
    Time: O(N), Space: O(1)
    """
    min_price = float("inf")
    max_profit = 0
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
    return max_profit


def run_tests():
    assert max_profit([7, 1, 5, 3, 6, 4]) == 5
    assert max_profit([7, 6, 4, 3, 1]) == 0
    assert max_profit([1, 2]) == 1
    assert max_profit([]) == 0
    return True

if __name__ == "__main__":
    run_tests()
    print("All tests passed for p13_best_time_to_buy_and_sell_stock!")
