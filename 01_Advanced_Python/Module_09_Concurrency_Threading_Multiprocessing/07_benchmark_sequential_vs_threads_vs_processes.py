#!/usr/bin/env python3
"""Module 09: Concurrency Benchmarking (Sequential vs Threads vs Processes).

This script runs side-by-side performance benchmarks for both I/O-bound
and CPU-bound workloads.
"""

from __future__ import annotations

import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

# ==========================================
# 1. Workload Definitions
# ==========================================

def io_task(duration: float = 0.05) -> float:
    """Simulates an I/O wait (network API or disk read)."""
    time.sleep(duration)
    return duration


def cpu_task(n: int = 4_000_000) -> int:
    """Simulates heavy CPU calculation."""
    count = 0
    for i in range(n):
        count += i % 7
    return count


# ==========================================
# 2. Benchmarking Harness
# ==========================================

def benchmark_io() -> None:
    print("=" * 65)
    print("  BENCHMARK 1: I/O-Bound Workload (8 Tasks x 50ms wait)")
    print("=" * 65)
    tasks = [0.05] * 8

    # Sequential
    start = time.perf_counter()
    _ = [io_task(t) for t in tasks]
    t_seq = time.perf_counter() - start

    # ThreadPool
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=8) as pool:
        _ = list(pool.map(io_task, tasks))
    t_thread = time.perf_counter() - start

    # ProcessPool
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as pool:
        _ = list(pool.map(io_task, tasks))
    t_proc = time.perf_counter() - start

    print(f"Sequential Duration : {t_seq:.4f}s (Baseline)")
    print(f"ThreadPool Duration : {t_thread:.4f}s ({t_seq / t_thread:.1f}x Speedup!) [WINNER: BEST FOR I/O]")
    print(f"ProcessPool Duration: {t_proc:.4f}s (Process spawn overhead)")


def benchmark_cpu() -> None:
    print("\n" + "=" * 65)
    print("  BENCHMARK 2: CPU-Bound Workload (4 Heavy Calculation Tasks)")
    print("=" * 65)
    tasks = [3_000_000] * 4

    # Sequential
    start = time.perf_counter()
    _ = [cpu_task(n) for n in tasks]
    t_seq = time.perf_counter() - start

    # ThreadPool (Constrained by GIL)
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        _ = list(pool.map(cpu_task, tasks))
    t_thread = time.perf_counter() - start

    # ProcessPool (Bypasses GIL across CPU cores)
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as pool:
        _ = list(pool.map(cpu_task, tasks))
    t_proc = time.perf_counter() - start

    print(f"Sequential Duration : {t_seq:.4f}s (Baseline)")
    print(f"ThreadPool Duration : {t_thread:.4f}s (No speedup due to GIL!)")
    print(f"ProcessPool Duration: {t_proc:.4f}s ({t_seq / t_proc:.1f}x Speedup!) [WINNER: BEST FOR CPU]")


def main() -> None:
    benchmark_io()
    benchmark_cpu()


if __name__ == "__main__":
    main()
