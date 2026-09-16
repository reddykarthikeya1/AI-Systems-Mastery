#!/usr/bin/env python3
"""Module 05: Generators & Iterators Demonstration.

This script demonstrates the Iterator Protocol (__iter__, __next__),
generator functions with yield, yield from sub-generators, and generator pipelines.
"""

from __future__ import annotations

from collections.abc import Generator, Iterator


class CountdownIterator:
    """Explicit class implementation of the Iterator Protocol."""

    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val


def prime_number_stream(limit: int) -> Generator[int, None, None]:
    """Infinite or capped generator yielding prime numbers lazily."""
    for num in range(2, limit + 1):
        for divisor in range(2, int(num ** 0.5) + 1):
            if num % divisor == 0:
                break
        else:
            yield num  # Pauses execution and returns prime


def combined_batch_generator() -> Generator[str, None, None]:
    """Demonstrates delegating sub-generators using 'yield from'."""
    yield from (f"Alpha Batch #{i}" for i in range(1, 3))
    yield from (f"Beta Batch #{i}" for i in range(1, 3))


def main() -> None:
    print("=" * 60)
    print("  1. Custom Iterator Protocol (CountdownIterator)")
    print("=" * 60)

    countdown = CountdownIterator(3)
    for step in countdown:
        print(f"  Step: {step}")

    print("\n" + "=" * 60)
    print("  2. Lazy Prime Number Generator Stream")
    print("=" * 60)

    primes = list(prime_number_stream(30))
    print(f"Primes up to 30: {primes}")

    print("\n" + "=" * 60)
    print("  3. Sub-Generator Delegation with 'yield from'")
    print("=" * 60)

    for batch in combined_batch_generator():
        print(f"  Processed: {batch}")


if __name__ == "__main__":
    main()
