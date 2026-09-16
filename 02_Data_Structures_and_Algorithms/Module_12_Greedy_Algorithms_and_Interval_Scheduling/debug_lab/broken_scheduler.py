#!/usr/bin/env python3
"""Greedy scheduler. Exits 0, and books overlapping meetings.

Read SYMPTOMS.md. Do not read ANSWERS.md until you have a diagnosis for each.
"""

from __future__ import annotations

import itertools

RULE = "=" * 68


def merge_intervals(intervals):
    if not intervals:
        return []
    ordered = sorted(intervals)
    out = [ordered[0]]
    for start, end in ordered[1:]:
        last_start, last_end = out[-1]
        if start <= last_end:
            out[-1] = (last_start, end)
        else:
            out.append((start, end))
    return out


def max_non_overlapping(intervals):
    if not intervals:
        return 0
    count = 0
    last_end = float("-inf")
    for start, end in sorted(intervals):
        if start >= last_end:
            count += 1
            last_end = end
    return count


def max_profit_stock(prices):
    cheapest = float("inf")
    best = 0
    for price in prices:
        if price < cheapest:
            cheapest = price
        if price - cheapest > best:
            best = int(price - cheapest)
    return best


def gas_station(gas, cost):
    start = 0
    tank = 0
    for i, (g, c) in enumerate(zip(gas, cost)):
        tank += g - c
        if tank < 0:
            start = i + 1
            tank = 0
    return start


def main() -> None:
    print(RULE)
    print("SCHEDULING SERVICE")
    print(RULE)

    print()
    print("[1] Merging calendar blocks")
    cases = [
        ([(1, 3), (2, 6), (8, 10), (15, 18)], [(1, 6), (8, 10), (15, 18)]),
        ([(1, 10), (2, 3)], [(1, 10)]),
        ([(1, 4), (2, 3)], [(1, 4)]),
        ([(1, 100), (2, 3), (4, 5)], [(1, 100)]),
    ]
    for intervals, expected in cases:
        print(f"      {intervals}")
        print(f"          reported {merge_intervals(intervals)}")
        print(f"          expected {expected}")

    print()
    print("[2] Maximum non-overlapping meetings")
    for intervals in ([(1, 3), (2, 4), (3, 5)], [(1, 10), (2, 3), (4, 5), (6, 7)],
                      [(0, 2), (1, 4), (3, 5), (4, 6)]):
        brute = 0
        for r in range(len(intervals) + 1):
            for combo in itertools.combinations(sorted(intervals, key=lambda iv: iv[1]), r):
                if all(a[1] <= b[0] for a, b in zip(combo, combo[1:])):
                    brute = max(brute, r)
        print(f"      {intervals} -> {max_non_overlapping(intervals)} (expected {brute})")

    print()
    print("[3] Best single trade")
    for prices in ([7, 1, 5, 3, 6, 4], [7, 6, 4, 3, 1], [9, 1], [2, 4, 1], [3, 3]):
        brute = max(
            (prices[j] - prices[i]
             for i in range(len(prices)) for j in range(i + 1, len(prices))),
            default=0,
        )
        print(f"      {prices} -> {max_profit_stock(prices)} (expected {max(brute, 0)})")

    print()
    print("[4] Gas station circuit start")
    cases = [([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]), ([2, 3, 4], [3, 4, 3]),
             ([4], [5]), ([3, 1, 1], [1, 2, 2])]
    for gas, cost in cases:
        def brute_start(g, c):
            n = len(g)
            for s in range(n):
                tank = 0
                for k in range(n):
                    i = (s + k) % n
                    tank += g[i] - c[i]
                    if tank < 0:
                        break
                else:
                    return s
            return -1
        print(f"      gas={gas} cost={cost} -> {gas_station(gas, cost)} "
              f"(expected {brute_start(gas, cost)})")

    print()
    print(RULE)
    print("Scheduling complete. Exit code 0.")
    print(RULE)


if __name__ == "__main__":
    main()
