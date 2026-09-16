"""Module 01: Interactive Complexity & Bit Manipulation CLI Sandbox."""
from __future__ import annotations


def demo_bit_tricks():
    print("\n" + "=" * 60)
    print("DEMO: Live Bitwise Magic")
    print("=" * 60)
    val = 12  # 0b1100
    print(f"Number: {val} (Binary: {bin(val)})")
    cleared = val & (val - 1)
    print(f"Clear lowest set bit: val & (val - 1) = {cleared} (Binary: {bin(cleared)})")
    print(f"Isolate lowest set bit: val & (-val) = {val & (-val)} (Binary: {bin(val & (-val))})")

    nums = [4, 1, 2, 1, 2]
    unique = 0
    for x in nums:
        unique ^= x
    print(f"\nXOR Single Number demo on {nums} -> Unique element: {unique}")


if __name__ == "__main__":
    demo_bit_tricks()
