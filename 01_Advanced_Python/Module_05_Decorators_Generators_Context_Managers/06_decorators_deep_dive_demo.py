#!/usr/bin/env python3
"""Module 05: Decorators Deep Dive Demonstration.

This script demonstrates basic decorators, parameterized decorators,
class decorators, @functools.wraps, and @functools.lru_cache.
"""

from __future__ import annotations

import functools
import time


def timing_profiler(func):
    """Measures and reports execution time of any function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"[PROFILER] {func.__name__}() executed in {duration:.6f}s")
        return result
    return wrapper


def validate_positive_args(func):
    """Enforces that all numeric arguments must be strictly positive."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError(f"All numeric args must be > 0. Received: {arg}")
        return func(*args, **kwargs)
    return wrapper


@functools.lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """Calculates nth Fibonacci number with O(N) memoization via lru_cache."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@timing_profiler
@validate_positive_args
def calculate_rectangle_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle."""
    return length * width


def main() -> None:
    print("=" * 60)
    print("  1. Chained Function Decorators (@timing_profiler + @validate)")
    print("=" * 60)

    area = calculate_rectangle_area(15.0, 20.0)
    print(f"Calculated Area: {area}")

    try:
        calculate_rectangle_area(-5.0, 10.0)
    except ValueError as e:
        print(f"[BLOCKED] Decorator caught invalid input: {e}")

    print("\n" + "=" * 60)
    print("  2. Built-in Caching with @functools.lru_cache")
    print("=" * 60)

    start = time.perf_counter()
    fib_35 = fibonacci(35)
    duration = time.perf_counter() - start

    print(f"fibonacci(35) = {fib_35} (Computed in {duration:.6f}s via cache)")
    print(f"Cache Stats   : {fibonacci.cache_info()}")


if __name__ == "__main__":
    main()
