"""Module 10: Interactive 1D DP CLI Sandbox."""
from __future__ import annotations


def demo():
    print("\n=== DEMO: Coin Change 1D DP Table Progression ===")
    coins = [1, 2, 5]
    amount = 11
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
    print(f"Fewest coins to make ${amount} with {coins}: {dp[amount]}")


if __name__ == "__main__":
    demo()
