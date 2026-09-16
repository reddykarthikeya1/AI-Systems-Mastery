#!/usr/bin/env python3
"""Module 03: Lists & Tuples Internals Demonstration.

This script demonstrates dynamic array growth, list comprehensions,
shallow vs deep copying, and tuple memory advantages.
"""

from __future__ import annotations

import copy
import sys
import time


def demo_list_growth() -> None:
    print("=" * 60)
    print("  1. List Dynamic Over-Allocation in Memory")
    print("=" * 60)

    lst: list[int] = []
    print(f"Empty list: {sys.getsizeof(lst)} bytes")

    sizes = []
    for i in range(15):
        lst.append(i)
        sizes.append((len(lst), sys.getsizeof(lst)))

    print(f"{'Elements':<10} | {'Bytes in RAM':<12}")
    print("-" * 26)
    for length, byte_size in sizes:
        print(f"{length:<10} | {byte_size:<12}")


def demo_comprehension_performance() -> None:
    print("\n" + "=" * 60)
    print("  2. List Comprehension vs For-Loop Performance")
    print("=" * 60)

    N = 1_000_000

    # 1. Standard for-loop with append
    start = time.perf_counter()
    loop_result = []
    for x in range(N):
        if x % 2 == 0:
            loop_result.append(x * 2)
    loop_duration = time.perf_counter() - start

    # 2. List comprehension (Executed at C-speed in bytecode)
    start = time.perf_counter()
    comp_result = [x * 2 for x in range(N) if x % 2 == 0]
    comp_duration = time.perf_counter() - start
    assert len(loop_result) == len(comp_result)

    print(f"For-loop append duration  : {loop_duration:.4f}s")
    print(f"List comprehension duration: {comp_duration:.4f}s")
    print(f"Comprehension was {loop_duration / comp_duration:.2f}x faster!")


def demo_shallow_vs_deep_copy() -> None:
    print("\n" + "=" * 60)
    print("  3. Shallow Copy vs Deep Copy")
    print("=" * 60)

    # Nested list containing sublists
    original = [[1, 2], [3, 4]]
    shallow = list(original)      # Or original.copy()
    deep = copy.deepcopy(original)

    # Modify nested inner element
    original[0][0] = 999

    print(f"Original after mutation: {original}")
    print(f"Shallow copy (MUTATED!) : {shallow}  <-- Shared nested reference!")
    print(f"Deep copy (PROTECTED)   : {deep}  <-- Completely isolated clone")


def demo_tuple_memory_efficiency() -> None:
    print("\n" + "=" * 60)
    print("  4. Tuple Memory & Immutability Advantages")
    print("=" * 60)

    sample_list = [10, 20, 30, 40, 50]
    sample_tuple = (10, 20, 30, 40, 50)

    print(f"List memory size  : {sys.getsizeof(sample_list)} bytes")
    print(f"Tuple memory size : {sys.getsizeof(sample_tuple)} bytes")
    print(f"Tuples use {sys.getsizeof(sample_list) - sys.getsizeof(sample_tuple)} fewer bytes per instance!")


def main() -> None:
    demo_list_growth()
    demo_comprehension_performance()
    demo_shallow_vs_deep_copy()
    demo_tuple_memory_efficiency()


if __name__ == "__main__":
    main()
