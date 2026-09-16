#!/usr/bin/env python3
"""Broken Log Analyzer demonstrating decorator, generator, and context manager traps."""

import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        res = func(*args, **kwargs)
        duration = time.perf_counter() - t0
        return res
    return wrapper

@timing_decorator
def parse_access_log(line: str) -> str:
    """Extract path from an Apache log line."""
    return line.split()[6]

def generate_log_lines():
    yield "GET /home HTTP/1.1"
    yield "POST /login HTTP/1.1"
    yield "GET /dashboard HTTP/1.1"

class SafeDatabaseTransaction:
    def __enter__(self):
        print("[DB] Transaction opened")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("[DB] Transaction closed")
        return True

if __name__ == "__main__":
    print(f"Function name: {parse_access_log.__name__} (Expected: 'parse_access_log', got 'wrapper'!)")

    stream = generate_log_lines()
    count1 = len(list(stream))
    count2 = len(list(stream))
    print(f"First pass count: {count1}, Second pass count: {count2} (Expected 3 both times!)")

    with SafeDatabaseTransaction():
        raise KeyError("Account record not found in ledger")
    print("Execution continued after critical KeyError was silently swallowed!")
