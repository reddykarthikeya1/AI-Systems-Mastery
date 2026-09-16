#!/usr/bin/env python3
"""Module 02: Scopes (LEGB) & Closures Demonstration.

This script demonstrates local vs enclosing vs global scopes,
the 'global' and 'nonlocal' keywords, and stateful closures.
"""

from __future__ import annotations

# Global variable
APP_NAME = "Python Scope Demo"
GLOBAL_COUNTER = 0


def demo_global_vs_local() -> None:
    print("=" * 60)
    print("  1. Global vs Local Scope & 'global' Keyword")
    print("=" * 60)

    def read_global() -> None:
        # Reading global is fine without any keyword
        print(f"Reading global APP_NAME: {APP_NAME}")

    def increment_global() -> None:
        global GLOBAL_COUNTER
        GLOBAL_COUNTER += 1
        print(f"Updated GLOBAL_COUNTER: {GLOBAL_COUNTER}")

    read_global()
    increment_global()
    increment_global()


def demo_enclosing_and_nonlocal() -> None:
    print("\n" + "=" * 60)
    print("  2. Enclosing Scope & 'nonlocal' Keyword")
    print("=" * 60)

    def make_counter(start: int = 0):
        # Enclosing variable in make_counter's frame
        count = start

        def counter() -> int:
            nonlocal count
            count += 1
            return count

        return counter

    counter_a = make_counter(0)
    counter_b = make_counter(100)

    print(f"counter_a: {counter_a()}")  # 1
    print(f"counter_a: {counter_a()}")  # 2
    print(f"counter_b: {counter_b()}")  # 101
    print(f"counter_a: {counter_a()}")  # 3 (counter_a retained its own state!)


def demo_closure_introspection() -> None:
    print("\n" + "=" * 60)
    print("  3. Closure Introspection (__closure__ and cell objects)")
    print("=" * 60)

    def multiplier_factory(factor: float):
        # 'factor' is captured by the inner closure
        def multiply(number: float) -> float:
            return number * factor
        return multiply

    triple = multiplier_factory(3.0)
    print(f"triple(10) = {triple(10.0)}")

    # Inspect the memory cell inside triple's closure backpack:
    if triple.__closure__:
        cell = triple.__closure__[0]
        print(f"Closure Cell Object : {cell}")
        print(f"Stored Factor Value : {cell.cell_contents}")


def main() -> None:
    demo_global_vs_local()
    demo_enclosing_and_nonlocal()
    demo_closure_introspection()


if __name__ == "__main__":
    main()
