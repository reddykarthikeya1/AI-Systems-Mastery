#!/usr/bin/env python3
"""Module 18: cProfile Bottleneck Profiling Demonstration.

This script demonstrates using Python's built-in cProfile profiler to pinpoint
slow function calls.
"""

from __future__ import annotations

import cProfile
import io
import pstats
import time


def simulate_network_query() -> str:
    time.sleep(0.05)
    return "DATABASE_RECORD"


def simulate_heavy_math() -> int:
    return sum(n * n for n in range(500_000))


def run_workload() -> None:
    for _ in range(3):
        simulate_network_query()
    simulate_heavy_math()


def main() -> None:
    print("=" * 60)
    print("  cProfile Performance Bottleneck Profiling Demo")
    print("=" * 60)

    pr = cProfile.Profile()
    pr.enable()
    run_workload()
    pr.disable()

    stream = io.StringIO()
    ps = pstats.Stats(pr, stream=stream).sort_stats("cumtime")
    ps.print_stats(10)

    print(stream.getvalue())


if __name__ == "__main__":
    main()
