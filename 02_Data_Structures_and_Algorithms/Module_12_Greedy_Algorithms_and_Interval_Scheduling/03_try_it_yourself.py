"""Module 12: Interactive Greedy CLI Sandbox."""
from __future__ import annotations


def demo():
    print("\n=== DEMO: Greedy Jump Game Max Reach ===")
    nums = [2, 3, 1, 1, 4]
    max_reach = 0
    for i, x in enumerate(nums):
        if i > max_reach:
            print("Stuck!")
            return
        max_reach = max(max_reach, i + x)
        print(f"At idx {i} (val {x}): max reachable index is now {max_reach}")
    print("Reached the end successfully!")


if __name__ == "__main__":
    demo()
