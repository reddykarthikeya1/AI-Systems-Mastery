"""Production solution for GridKnapsackDPEngine."""
from __future__ import annotations


class GridKnapsackDPEngine:
    """2D Dynamic programming algorithms with item reconstruction and space optimization."""

    @staticmethod
    def knapsack_01(weights: list[int], values: list[int], capacity: int) -> tuple[int, list[int]]:
        n = len(weights)
        if n == 0 or capacity <= 0:
            return 0, []

        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            w = weights[i - 1]
            v = values[i - 1]
            for c in range(capacity + 1):
                if w <= c:
                    dp[i][c] = max(dp[i - 1][c], dp[i - 1][c - w] + v)
                else:
                    dp[i][c] = dp[i - 1][c]

        max_value = dp[n][capacity]

        # Reconstruct chosen items
        selected_indices: list[int] = []
        c = capacity
        for i in range(n, 0, -1):
            if dp[i][c] != dp[i - 1][c]:
                selected_indices.append(i - 1)
                c -= weights[i - 1]

        selected_indices.reverse()
        return max_value, selected_indices

    @staticmethod
    def longest_common_subsequence(text1: str, text2: str) -> int:
        """LCS with O(min(N, M)) memory footprint."""
        if len(text1) < len(text2):
            text1, text2 = text2, text1

        m, n = len(text1), len(text2)
        prev = [0] * (n + 1)
        curr = [0] * (n + 1)

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    curr[j] = prev[j - 1] + 1
                else:
                    curr[j] = max(prev[j], curr[j - 1])
            prev = list(curr)

        return prev[n]

    @staticmethod
    def edit_distance(word1: str, word2: str) -> int:
        """Levenshtein minimum edit distance."""
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],    # deletion
                        dp[i][j - 1],    # insertion
                        dp[i - 1][j - 1] # replacement
                    )

        return dp[m][n]
