"""Module 05: Interactive Foundations Interactive Decorators & Generators Playground.

Run this script directly in your terminal:
    python try_it_yourself.py
"""

import time


def timing_decorator(func):
    """A simple decorator measuring how long a function takes."""
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        print(f"[TIME]  [{func.__name__}] finished in {elapsed * 1000:.3f} ms")
        return result
    return wrapper

@timing_decorator
def calculate_sum(n):
    return sum(range(n))

def number_stream(max_val):
    """Generator yielding numbers one by one."""
    curr = 1
    while curr <= max_val:
        yield curr
        curr += 1

def main():
    print("=" * 60)
    print("  MODULE 05: DECORATORS & GENERATORS PLAYGROUND [TIME]")
    print("=" * 60)

    print("\n1. Testing @timing_decorator on sum calculation:")
    ans = calculate_sum(500_000)
    print(f"Sum of first 500,000 numbers: {ans:,}")

    print("\n2. Testing number_stream() Generator (One at a time):")
    stream = number_stream(5)
    for val in stream:
        print(f"  Received next value from generator: {val}")
        time.sleep(0.15)

    print("\nNotice how the generator produced values lazily on demand!")
    print("Proceed to Module 06.")

if __name__ == "__main__":
    main()
