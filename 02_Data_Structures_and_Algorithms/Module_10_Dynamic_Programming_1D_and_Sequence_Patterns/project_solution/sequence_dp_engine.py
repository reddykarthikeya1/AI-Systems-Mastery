"""Production solution for SequenceDPEngine."""
from __future__ import annotations

import bisect


class SequenceDPEngine:
    """1D sequence dynamic programming with reconstruction."""

    @staticmethod
    def longest_increasing_subsequence(nums: list[int]) -> tuple[int, list[int]]:
        """O(N log N) patience sorting with parent-pointer path reconstruction."""
        if not nums:
            return 0, []

        tails: list[int] = []          # Smallest tail of all increasing subseqs of length i+1
        tail_indices: list[int] = []  # Index in nums corresponding to tails
        parent: list[int] = [-1] * len(nums)

        for i, x in enumerate(nums):
            idx = bisect.bisect_left(tails, x)
            if idx == len(tails):
                tails.append(x)
                tail_indices.append(i)
            else:
                tails[idx] = x
                tail_indices[idx] = i

            if idx > 0:
                parent[i] = tail_indices[idx - 1]

        # Reconstruct path from the last element
        lis_length = len(tails)
        curr = tail_indices[-1]
        reconstructed: list[int] = []
        while curr != -1:
            reconstructed.append(nums[curr])
            curr = parent[curr]

        reconstructed.reverse()
        return lis_length, reconstructed

    @staticmethod
    def coin_change_min_coins(coins: list[int], amount: int) -> tuple[int, list[int]]:
        """Min coins DP with explicit coin combination reconstruction."""
        if amount == 0:
            return 0, []
        if amount < 0:
            return -1, []

        dp = [float("inf")] * (amount + 1)
        parent_coin = [-1] * (amount + 1)
        dp[0] = 0

        for i in range(1, amount + 1):
            for c in coins:
                if i - c >= 0 and dp[i - c] + 1 < dp[i]:
                    dp[i] = dp[i - c] + 1
                    parent_coin[i] = c

        if dp[amount] == float("inf"):
            return -1, []

        reconstructed: list[int] = []
        curr = amount
        while curr > 0:
            c = parent_coin[curr]
            reconstructed.append(c)
            curr -= c

        return int(dp[amount]), reconstructed

    @staticmethod
    def word_break(s: str, word_dict: list[str]) -> bool:
        """DP boolean array word break in O(N * max_word_len)."""
        words = set(word_dict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True

        for i in range(1, n + 1):
            for j in range(max(0, i - 20), i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break

        return dp[n]
