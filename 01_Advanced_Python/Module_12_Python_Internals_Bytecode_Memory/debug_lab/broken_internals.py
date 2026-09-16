#!/usr/bin/env python3
"""Broken Internals Profiler demonstrating reference cycles, sys.getsizeof, and ctypes traps."""

import gc
import sys

class Node:
    def __init__(self, name: str):
        self.name = name
        self.link = None

    def __del__(self):
        print(f"[GC] Node {self.name} finalized")

def create_reference_cycle():
    a = Node("A")
    b = Node("B")
    a.link = b
    b.link = a
    del a
    del b

def inspect_memory_footprint():
    # It returns only the size of the container pointers, NOT the referenced items.
    small_list = [1, 2, 3]
    large_list = ["A" * 10_000, "B" * 10_000, "C" * 10_000]
    
    print(f"Small list getsizeof: {sys.getsizeof(small_list)} bytes")
    print(f"Large list getsizeof: {sys.getsizeof(large_list)} bytes (Virtually identical!)")

if __name__ == "__main__":
    print("Testing reference cycles:")
    gc.disable()  # Simulate disabled cyclic GC
    create_reference_cycle()
    print("Deleted cycle references without cyclic GC collection.")

    inspect_memory_footprint()
