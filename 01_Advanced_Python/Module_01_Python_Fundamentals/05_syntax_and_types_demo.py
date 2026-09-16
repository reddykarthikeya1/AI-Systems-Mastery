#!/usr/bin/env python3
"""Module 01: Syntax, Primitive Types & Memory Demonstration.

This script demonstrates Python's dynamic typing, variable memory IDs,
arithmetic mechanics, float precision, and modern string formatting.
"""

from __future__ import annotations

import math
from decimal import Decimal


def demo_variables_and_memory() -> None:
    print("=" * 60)
    print("  1. Variables as Memory Tags & Dynamic Typing")
    print("=" * 60)

    # Initial assignment
    data = 42
    print(f"data = {data!r:<15} | Type: {type(data).__name__:<10} | id: {id(data)}")

    # Reassignment to float
    data = 3.14159
    print(f"data = {data!r:<15} | Type: {type(data).__name__:<10} | id: {id(data)}")

    # Reassignment to string
    data = "Hello, Python!"
    print(f"data = {data!r:<15} | Type: {type(data).__name__:<10} | id: {id(data)}")


def demo_arithmetic_and_division() -> None:
    print("\n" + "=" * 60)
    print("  2. Division & Arithmetic Nuances")
    print("=" * 60)

    numerator = 17
    denominator = 5

    true_div = numerator / denominator    # Always returns a float
    floor_div = numerator // denominator  # Truncates to nearest smaller whole number
    modulo = numerator % denominator      # Remainder
    power = denominator ** 3             # 5^3 = 125

    print(f"{numerator} /  {denominator} = {true_div}  (True Division - float)")
    print(f"{numerator} // {denominator} = {floor_div}        (Floor Division - int)")
    print(f"{numerator} %  {denominator} = {modulo}        (Modulo / Remainder)")
    print(f"{denominator} ** 3  = {power}      (Exponentiation / Power)")
    print(f"Verification: {denominator} * {floor_div} + {modulo} == {denominator * floor_div + modulo}")


def demo_floating_point_precision() -> None:
    print("\n" + "=" * 60)
    print("  3. Floating-Point Binary Representation vs Decimals")
    print("=" * 60)

    val1 = 0.1
    val2 = 0.2
    total = val1 + val2

    print(f"0.1 + 0.2 in standard float : {total:.17f}")
    print(f"Does 0.1 + 0.2 == 0.3?       : {total == 0.3}")
    print(f"Using math.isclose(total, 0.3): {math.isclose(total, 0.3)}")

    # Exact decimal representation:
    dec1 = Decimal("0.1")
    dec2 = Decimal("0.2")
    dec_total = dec1 + dec2
    print(f"Decimal('0.1') + Decimal('0.2') == Decimal('0.3'): {dec_total == Decimal('0.3')}")


def demo_identity_vs_equality() -> None:
    print("\n" + "=" * 60)
    print("  4. Identity ('is') vs Equality ('==')")
    print("=" * 60)

    # Lists are mutable containers
    list_one = [10, 20, 30]
    list_two = [10, 20, 30]

    print(f"list_one == list_two : {list_one == list_two} (Same values)")
    print(f"list_one is list_two : {list_one is list_two} (Different memory locations)")

    alias = list_one
    print(f"list_one is alias    : {list_one is alias} (Same memory location)")

    # None check best practice
    mystery_value = None
    print(f"mystery_value is None: {mystery_value is None}")


def demo_string_slicing_and_formatting() -> None:
    print("\n" + "=" * 60)
    print("  5. String Slicing & Modern f-Strings")
    print("=" * 60)

    text = "PythonMastery2026"
    print(f"Original String : {text}")
    print(f"Slice [0:6]     : {text[0:6]} (First 6 characters)")
    print(f"Slice [6:13]    : {text[6:13]} (Middle segment)")
    print(f"Slice [13:]     : {text[13:]} (End segment)")
    print(f"Slice [::-1]    : {text[::-1]} (Reversed)")

    # Formatted Currency and Percentages
    revenue = 4850920.456
    growth = 0.2458
    print(f"\nRevenue: ${revenue:,.2f} | Year-over-Year Growth: {growth:.1%}")


def main() -> None:
    demo_variables_and_memory()
    demo_arithmetic_and_division()
    demo_floating_point_precision()
    demo_identity_vs_equality()
    demo_string_slicing_and_formatting()
    print("\n[Done] Syntax and Types Demonstration completed successfully!")


if __name__ == "__main__":
    main()
