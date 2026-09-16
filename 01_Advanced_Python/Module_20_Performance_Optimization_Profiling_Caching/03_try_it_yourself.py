"""
Module 20: Performance Benchmark - Cached vs Uncached
Run: python try_it_yourself.py
"""

import functools
import time


def slow_fib(n):
    if n < 2:
        return n
    return slow_fib(n - 1) + slow_fib(n - 2)


@functools.lru_cache(maxsize=128)
def fast_fib(n):
    if n < 2:
        return n
    return fast_fib(n - 1) + fast_fib(n - 2)


def main():
    print("=" * 60)
    print("  MODULE 20: CACHING & PERFORMANCE PLAYGROUND [*]")
    print("=" * 60)

    N = 30
    print(f"\n1. Computing Fibonacci({N}) WITHOUT caching:")
    t0 = time.time()
    ans1 = slow_fib(N)
    elapsed_slow = time.time() - t0
    print(f"  Result: {ans1} (Time: {elapsed_slow:.4f}s)")

    print(f"\n2. Computing Fibonacci({N}) WITH @lru_cache:")
    t0 = time.time()
    ans2 = fast_fib(N)
    elapsed_fast = time.time() - t0
    print(f"  Result: {ans2} (Time: {elapsed_fast:.6f}s)")

    if elapsed_fast > 0:
        speedup = elapsed_slow / max(elapsed_fast, 1e-9)
        print(f"\n[OK] Speedup factor: {speedup:,.1f}x faster with caching!")


if __name__ == "__main__":
    main()
