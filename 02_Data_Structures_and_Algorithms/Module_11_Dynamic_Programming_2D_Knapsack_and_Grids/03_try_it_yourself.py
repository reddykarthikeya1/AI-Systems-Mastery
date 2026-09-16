"""Module 11: Interactive 2D DP CLI Sandbox."""
from __future__ import annotations


def demo():
    print("\n=== DEMO: Grid Paths 2D Table ===")
    m, n = 3, 3
    dp = [[1] * n for _ in range(m)]
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
    print(f"Unique paths on a {m}x{n} grid: {dp[m-1][n-1]}")


if __name__ == "__main__":
    demo()
