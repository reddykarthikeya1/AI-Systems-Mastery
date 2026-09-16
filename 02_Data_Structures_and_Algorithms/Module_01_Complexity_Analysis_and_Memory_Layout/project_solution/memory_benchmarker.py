"""Production solution for MemoryBenchmarker."""
from __future__ import annotations

import time
import tracemalloc
from collections.abc import Callable
from typing import Any


class MemoryBenchmarker:
    """Empirical complexity and memory allocation profiler."""

    @staticmethod
    def measure_runtime_ns(func: Callable[..., Any], *args: Any, **kwargs: Any) -> tuple[Any, int]:
        """Execute func and return (result, duration_in_nanoseconds)."""
        t0 = time.perf_counter_ns()
        result = func(*args, **kwargs)
        t1 = time.perf_counter_ns()
        return result, t1 - t0

    @staticmethod
    def measure_peak_memory_bytes(
        func: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> tuple[Any, int]:
        """Execute func under tracemalloc and return (result, peak_bytes)."""
        tracemalloc.start()
        try:
            result = func(*args, **kwargs)
            _, peak = tracemalloc.get_traced_memory()
            return result, peak
        finally:
            tracemalloc.stop()

    @staticmethod
    def check_growth_rate(timings: list[tuple[int, float]]) -> str:
        """Analyze (input_size, elapsed_time) pairs and classify growth as O(1), O(N), or O(N^2)."""
        if len(timings) < 2:
            return "O(1)"

        # Sort by input size
        sorted_points = sorted(timings, key=lambda x: x[0])
        n1, t1 = sorted_points[0]
        n2, t2 = sorted_points[-1]

        if n1 <= 0 or n2 <= 0 or t1 <= 0 or t2 <= 0:
            return "O(1)"

        size_ratio = n2 / n1
        time_ratio = t2 / t1

        if time_ratio < 1.5:
            return "O(1)"
        elif time_ratio <= size_ratio * 1.8:
            return "O(N)"
        else:
            return "O(N^2)"
