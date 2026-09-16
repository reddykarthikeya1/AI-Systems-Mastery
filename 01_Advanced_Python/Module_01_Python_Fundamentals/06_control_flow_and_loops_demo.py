#!/usr/bin/env python3
"""Module 01: Control Flow, Pattern Matching & Loops Demonstration.

This script demonstrates if-elif-else branches, Python 3.10+ match-case,
range loops, while loops, and loop-else search patterns.
"""

from __future__ import annotations


def demo_if_elif_else(credit_score: int) -> str:
    """Categorize a credit score into loan eligibility tiers."""
    if credit_score >= 750:
        return "Tier 1 (Prime Rate: 4.5%)"
    elif credit_score >= 680:
        return "Tier 2 (Standard Rate: 6.2%)"
    elif credit_score >= 600:
        return "Tier 3 (Subprime Rate: 9.8%)"
    else:
        return "Ineligible (Score below minimum threshold)"


def demo_pattern_matching(command: str) -> None:
    """Demonstrate Python 3.10+ match-case structural pattern matching."""
    match command.strip().lower().split():
        case ["deposit", amount_str]:
            try:
                amt = float(amount_str)
                print(f"[ACTION] Depositing ${amt:,.2f} into account.")
            except ValueError:
                print(f"[ERROR] Invalid amount: {amount_str}")
        case ["withdraw", amount_str]:
            try:
                amt = float(amount_str)
                print(f"[ACTION] Withdrawing ${amt:,.2f} from account.")
            except ValueError:
                print(f"[ERROR] Invalid amount: {amount_str}")
        case ["balance"] | ["check", "balance"]:
            print("[ACTION] Current balance: $12,450.00")
        case ["exit"] | ["quit"]:
            print("[ACTION] Exiting system session.")
        case _:
            print(f"[ERROR] Unrecognized command: '{command}'")


def demo_for_and_while_loops() -> None:
    print("=" * 60)
    print("  1. Loops: Generating Ranges and Accumulation")
    print("=" * 60)

    # Accumulate sum of first 10 integers (1 to 10)
    total = 0
    for num in range(1, 11):
        total += num
    print(f"Sum of numbers from 1 to 10: {total}")

    # While loop with countdown
    print("\nWhile Loop Countdown:")
    timer = 3
    while timer > 0:
        print(f"  T-minus {timer}...")
        timer -= 1
    print("  Launch! [Blastoff]")


def demo_loop_else_search() -> None:
    print("\n" + "=" * 60)
    print("  2. The Loop 'else' Search Pattern")
    print("=" * 60)

    numbers_to_search = [14, 21, 35, 42, 56]
    target_divisor = 11

    # Search for an item divisible by target_divisor
    for item in numbers_to_search:
        if item % target_divisor == 0:
            print(f"Found match: {item} is divisible by {target_divisor}")
            break
    else:
        # Runs ONLY if the loop finishes naturally with NO break!
        print(f"No numbers in {numbers_to_search} are divisible by {target_divisor}.")


def main() -> None:
    print("=== Credit Tier Evaluation ===")
    print(f"Score 780 -> {demo_if_elif_else(780)}")
    print(f"Score 640 -> {demo_if_elif_else(640)}")
    print(f"Score 550 -> {demo_if_elif_else(550)}")

    print("\n=== Match-Case Pattern Matching ===")
    demo_pattern_matching("deposit 500.50")
    demo_pattern_matching("withdraw 120")
    demo_pattern_matching("check balance")
    demo_pattern_matching("transfer 1000")

    demo_for_and_while_loops()
    demo_loop_else_search()


if __name__ == "__main__":
    main()
