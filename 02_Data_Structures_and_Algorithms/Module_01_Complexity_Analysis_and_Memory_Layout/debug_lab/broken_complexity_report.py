#!/usr/bin/env python3
"""A capacity-planning report. Runs clean, exits 0, and mis-sizes your servers.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

import math

RULE = "=" * 68


def classify_growth(timings: list[tuple[int, float]]) -> str:
    if len(timings) < 2:
        return "O(1)"
    first_size, first_time = timings[0]
    last_size, last_time = timings[-1]
    ratio = last_time / first_time
    if ratio < 1.5:
        return "O(1)"
    if ratio < 3.0:
        return "O(n)"
    return "O(n^2)"


def total_copies_for_appends(n: int, initial_capacity: int = 1) -> int:
    if n <= 0:
        return 0
    copies = 0
    capacity = initial_capacity
    size = 0
    while size < n:
        if size == capacity:
            copies += capacity
            capacity *= 2
        size += 1
    return copies


def max_binary_search_comparisons(n: int) -> int:
    if n <= 0:
        return 0
    return int(math.log2(n)) + 1


def count_pair_iterations(n: int) -> int:
    if n <= 1:
        return 0
    return n * (n - 1) / 2


def fits_budget(n: int, complexity: str, budget: int = 10**8) -> bool:
    log_n = max(1, int(math.log2(n)))
    if complexity == "O(1)":
        ops = 1
    elif complexity == "O(log n)":
        ops = log_n
    elif complexity == "O(n)":
        ops = n
    elif complexity == "O(n log n)":
        ops = n * log_n
    elif complexity == "O(n^2)":
        ops = n * n
    else:
        return False
    return ops <= budget


def main() -> None:
    print(RULE)
    print("CAPACITY PLANNING REPORT")
    print(RULE)

    print()
    print("[1] Growth classification from measured timings")
    samples = {
        "index_lookup": [(1000, 0.0010), (2000, 0.0010), (4000, 0.0011)],
        "linear_scan": [(1000, 0.0010), (2000, 0.0020), (4000, 0.0040)],
        "pairwise_join": [(1000, 0.0010), (2000, 0.0040), (4000, 0.0160)],
        "noisy_linear": [(1000, 0.0010), (2000, 0.0021), (4000, 0.0039)],
    }
    for name, timings in samples.items():
        print(f"      {name:<16} -> {classify_growth(timings)}")

    print()
    print("[2] Amortised append cost")
    for n in (5, 1000, 100_000):
        copies = total_copies_for_appends(n)
        print(f"      n={n:<8} total element copies = {copies:<10} "
              f"per-append average = {copies / n:.3f}")
    print("      (the claim is that the average is bounded by a constant)")

    print()
    print("[3] Binary search worst case")
    for n in (1, 8, 1024, 10**6, 10**18):
        print(f"      n={n:<20} comparisons = {max_binary_search_comparisons(n)}")

    print()
    print("[4] Pairwise comparison counts")
    for n in (4, 1000, 10**9):
        result = count_pair_iterations(n)
        print(f"      n={n:<12} comparisons = {result!r:<24} type={type(result).__name__}")

    print()
    print("[5] Does the proposed algorithm fit the budget?")
    checks = [
        (100_000, "O(n log n)"),
        (100_000, "O(n^2)"),
        (10**9, "O(n)"),
        (10, "O(n!)"),
        (10, "O(n^4)"),
    ]
    for n, complexity in checks:
        print(f"      n={n:<10} {complexity:<12} fits = {fits_budget(n, complexity)}")

    print()
    print(RULE)
    print("Report complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
