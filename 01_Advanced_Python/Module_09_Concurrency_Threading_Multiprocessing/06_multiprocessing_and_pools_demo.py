#!/usr/bin/env python3
"""Module 09: Multi-Processing & Process Pools Demonstration.

This script demonstrates CPU parallelism across multiple cores,
ProcessPoolExecutor, and IPC (Inter-Process Communication).
"""

from __future__ import annotations

import os
import time
from concurrent.futures import ProcessPoolExecutor


def cpu_heavy_factorial_sum(n: int) -> int:
    """CPU-intensive calculation executing in an isolated process."""
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total


def main() -> None:
    print("=" * 60)
    print("  1. Multiprocessing Across Multiple CPU Cores")
    print("=" * 60)

    print(f"Host Machine Logical CPU Cores : {os.cpu_count()}")
    print(f"Main Process PID               : {os.getpid()}")

    workloads = [5_000_000, 6_000_000, 7_000_000, 8_000_000]

    # ProcessPoolExecutor distributes tasks across separate OS processes
    start = time.perf_counter()
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(cpu_heavy_factorial_sum, workloads))
    duration = time.perf_counter() - start

    print(f"\nCalculated {len(results)} heavy CPU tasks in parallel: {duration:.4f}s")
    for idx, (workload, res) in enumerate(zip(workloads, results, strict=True), start=1):
        print(f"  Task #{idx} (N={workload:,}) -> Sum Result: {res}")


if __name__ == "__main__":
    # CRITICAL: On Windows, multiprocessing MUST be guarded inside if __name__ == '__main__':
    main()
